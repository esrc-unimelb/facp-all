import unittest

from pyramid import testing
from pyramid.paster import get_appsettings
from pyramid.httpexceptions import HTTPNotFound

from lxml import etree
from facp import FACP
from config import Config

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.request.registry.settings = get_appsettings('development.ini')
        self.request.matchdict['entity'] = 'E000180'

        self.facp = FACP(self.request)

        conf = Config(self.request, 'FCVC')
        source_document = "%s/%s.xml" % (conf.eac_data, self.facp.entity)
        self.tree = etree.parse(source_document)

    def tearDown(self):
        testing.tearDown()

    def test_config(self):
        conf = Config(self.request, 'FCVC')
        self.assertEqual(conf.eac_data, '/srv/ha/web/FCVC/LIVE/eac')
        self.assertNotEqual(conf.eac_data, '')

    def test_facp_init(self):
        self.assertEqual(self.facp.entity, 'E000180')
        self.assertNotEqual(self.facp.entity, 'E000181')

    def test_routes(self):
        self.request.matchdict['entity'] = 'AE00101'
        self.request.matchdict['state'] = 'act'
        facp = FACP(self.request)
        data = facp.page()
        self.assertEqual(data['doc']['EAC data path'], '/srv/ha/web/FCAC/LIVE/eac')
        data = facp.page_json()
        self.assertEqual(data['doc']['EAC data path'], '/srv/ha/web/FCAC/LIVE/eac')

        self.request.matchdict['entity'] = 'QE00392'
        self.request.matchdict['state'] = 'qld'
        facp = FACP(self.request)
        with self.assertRaises(HTTPNotFound):
            data = self.facp.page()
        with self.assertRaises(HTTPNotFound):
            data = self.facp.page_json()

    def test_get_page(self):
        conf = Config(self.request, 'FCVC')
        data = self.facp.get_page(conf.eac_data)
        data = data['doc']
        self.assertEqual(data['EAC data path'], '/srv/ha/web/FCVC/LIVE/eac')
        self.assertNotEqual(data['EAC data path'], '')

        self.request.matchdict['entity'] = 'Exxxxxxx'
        facp = FACP(self.request)
        with self.assertRaises(HTTPNotFound):
            data = facp.get_page(conf.eac_data)

    def test_get(self):
        # test we can get the data out of an element
        result = self.facp.get(self.tree, '/e:eac-cpf/e:control/e:recordId')
        self.assertEqual(result, 'E000180')
        self.assertNotEqual(result, 'E000181')

        # test we can get a list of element data out
        result = self.facp.get(self.tree, '//e:cpfRelation')
        self.assertIs(type(result), str)

        # test we can get the data out of an attribute
        result = self.facp.get(self.tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:fromDate', attrib='standardDate')
        self.assertEqual(result, '1853-01-01')
        self.assertNotEqual(result, '1854')

        # test we get an etree element 
        result = self.facp.get(self.tree, '/e:eac-cpf', element=True)
        self.assertIs(result.__class__, list)

    def test_get_xml(self):
        result = self.facp.get_xml('http://www.findandconnect.gov.au/vic/biogs/E000116b.htm')
        self.assertEqual(result, 'http://www.findandconnect.gov.au/ref/vic/eac/E000116.xml')
        self.assertNotEqual(result, '')

        result = self.facp.get_xml('http://www.findandconnect.gov.au/vic/biogs/nogo.htm')
        self.assertEqual(result, '')

    def test_get_header(self):
        result = self.facp.get_header(self.tree)
        self.assertEqual(result['state'], 'Victoria')
        self.assertNotEqual(result['state'], 'NSW')
        self.assertEqual(result['from'], '1853')

    def test_get_relations(self):
        result = self.facp.get_relations_earlier(self.tree)
        self.assertEqual(result['to'], '1853')

        result = self.facp.get_relations_later(self.tree)
        self.assertEqual(result['to'], '1965')

    def test_get_glossary_terms(self):
        result = self.facp.get_glossary_terms(self.tree)
        self.assertEqual(result, [{'href': '/guide/vic/E000116', 'id': 'E000116', 'name': 'Orphanage'}])

    def test_get_images(self):
        result = self.facp.get_images(self.tree)
        self.assertEqual(result[0][0]['dobject_page'], '/ref/vic/objects/D00000304.htm')

    def test_get_locations(self):
        result = self.facp.get_locations(self.tree)
        self.assertEqual(result[0]['to'], '1878')
        self.assertEqual(result[0]['from'], '1856')

    def test_get_records(self):
        result = self.facp.get_records(self.tree)
        self.assertEqual(result[0]['link'], '/guide/vic/E000734')


