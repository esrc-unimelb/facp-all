from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.view import notfound_view_config
from pyramid.httpexceptions import HTTPNotFound

import sys
import time
import datetime
import itertools
import urlparse
from lxml import etree

from config import Config

import logging
log = logging.getLogger('eacdatasource')

@view_defaults(request_method='GET', renderer='FACP/home.mak')
class FACP:
    def __init__(self, request):
        self.request = request
        self.entity = str(request.matchdict['entity'])

        self.code = {
            'act':       'FCAC',
            'australia': 'FCNA',
            'nsw':       'FCNS',
            'nt':        'FCNT',
            'qld':       'FCQD',
            'sa':        'FCSA',
            'tas':       'FCTS',
            'vic':       'FCVC',
            'wa':        'FCWA',
        }
        self.state = {
            'FCAC': 'act',
            'FCNA': 'australia',
            'FCNS': 'nsw',
            'FCNT': 'nt',
            'FCQD': 'qld',
            'FCSA': 'sa',
            'FCTS': 'tas',
            'FCVC': 'vic',
            'FCWA': 'wa'
        }

        # an array of sources used to compile the entry
        self.sources = []

    @view_config(route_name='page')
    def page(self):
        state = self.request.matchdict['state']
        c = Config(self.request, self.code[state])
        self.conf = c.load()
        return self.get_page()

    @view_config(route_name='page_json', renderer='json')
    def page_json(self):
        state = self.request.matchdict['state']
        c = Config(self.request, self.code[state])
        self.conf = c.load()
        return self.get_content()

    def get_page(self):
        source_document = "%s/%s.xml" % (self.conf.eac, self.entity)
        try:
            tree = etree.parse(source_document)
        except IOError:
            log.error("get_page: Couldn't read: %s" % source_document)
            raise HTTPNotFound
 
        # figure out which renderer to use - this is completely dependent
        #  on the entity type
        localType = self.get(tree, '/e:eac-cpf/e:control/e:localControl/e:term')
        if localType == 'Organisation':
            function = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:functions/e:function/e:term')
            if 'Home' not in function:
                log.debug("Setting template to: %s:" % 'FACP/other.mak')
                self.request.override_renderer = 'FACP/other.mak'

        elif localType in [ 'Archival Series', 'Archival Item', 'Archival Collection' ]:
            log.debug("Setting template to: %s:" % 'FACP/archival.mak')
            self.request.override_renderer = 'FACP/archival.mak'

        elif localType == 'Person':
            log.debug("Setting template to: %s:" % 'FACP/person.mak')
            self.request.override_renderer = 'FACP/person.mak'

        else:
            log.debug("Setting template to: %s:" % 'FACP/other.mak')
            self.request.override_renderer = 'FACP/other.mak'

        return self.get_content()

    def get_content(self):
        t1 = time.time()

        log.debug("EAC data location: %s" % self.conf.eac)
        log.debug("Entity: %s/%s.xml" % (self.conf.eac, self.entity))

        source_document = "%s/%s.xml" % (self.conf.eac, self.entity)
        try:
            tree = etree.parse(source_document)
        except IOError:
            log.error("get_content: Couldn't read: %s" % source_document)
            raise HTTPNotFound
        #print tree  
        href = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:entityId[1]')
        href = self.get_xml(href)

        doc = {
            'EAC data path': self.conf.eac,
            'Entity': "%s/%s.xml" % (self.conf.eac, self.entity),
            'locations': self.get_locations(tree),
            'header': self.get_header(tree),
            'summary': self.get_summary(tree),
            'glossary': self.get_glossary_terms(tree),
            'records': self.get_records(tree),
            'images': self.get_images(tree),
            'sources': self.sources,
        }

        t2 = time.time()
        doc['Time to Prepare Document'] = "%s" % (t2 - t1)
        log.debug("Time taken to prepare data '/{code}/{entity}': %s" % (t2 - t1))

        return { 'doc': doc }

    def get_source_info(self, xml_doc):
        source = {}
        try:
            tree = etree.parse(xml_doc)
            source['eid'] = self.get(tree, '/e:eac-cpf/e:control/e:recordId')
            source['etitle'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:nameEntry[1]/e:part')
            source['eweb'] = self.get_guide_url(source['eid'], self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:entityId[1]'))
            source['etype'] = self.get(tree, '/e:eac-cpf/e:control/e:localControl/e:term')
            source['esource'] = xml_doc
        except IOError:
            log.error("get_source_info: Couldn't read: %s" % xml_doc)
        return source

    def get(self, tree, path, attrib=None, element=None):
        """Extract data from an etree tree

        Helper to run an xpath against an etree tree. Can extract
        node (element) text, attribute data or just return an etree
        element for further processing.

        @params:
        tree: an etree tree
        path: an xpath expression to run against the tree
        attrib: if defined, the attribute date to extract from the element found
            via the xpath expression
        element: if set to True, return the etree element rather than the textual
            content of the node. Useful for performing further operations against.

        @returns:
        Either a single value or a list
        """
        result = tree.xpath(path, namespaces={ 'e': 'urn:isbn:1-931666-33-4', 'f': 'urn:isbn:1-931666-22-9' })
        if len(result) == 0:
            return ''

        # return the etree element reference
        if element is not None:
            return result

        # return the requested attribute
        elif attrib is not None:
            return result[0].attrib[attrib]
            #return tree.xpath(path, namespaces={ 'e': 'urn:isbn:1-931666-33-4' })[0].attrib[attrib]

        # otherwise - return the text content of the node
        else:
            try:
                #print "**", result, len(result)
                if len(result) == 1:
                    return result[0].text
                else:
                    return ', '.join([ e.text for e in result if e.text is not None ])
            except IndexError:
                log.error("Path: %s:" % path)
                log.error("Result: %s" % tree.xpath(path, namespaces={ 'e': 'urn:isbn:1-931666-33-4' }))

    def get_xml(self, href):
        """Given a href, find the corresponding XML data file.

        @params:
        href: a URL to a resource.o

        @returns:
        a URL to the XML file for that resource
        """
        try:
            tree = etree.parse(self.resolve(href), etree.HTMLParser())
            resource = tree.xpath('//meta[@name="EAC"]')[0].attrib['content']
            if not resource in self.sources:
                source = self.get_source_info(self.resolve(resource))
                existing_sources = [ s['esource'] for s in self.sources ]
                if source['esource'] not in existing_sources:
                    self.sources.append(source)
                    self.sources.sort(key=lambda source: source['etype'])
            return self.resolve(resource)
        except IOError:
            log.error("get_xml: Couldn't read: %s" % self.resolve(href))
            return ""

    def get_header(self, tree):
        """ Construct the header for the focus entity

        @params:
        tree: the etree tree to process
        """
        header = {}
        header['today'] = datetime.datetime.strftime(datetime.date.today(), "%d %B %Y")
        header['localtype'] = self.get(tree, '/e:eac-cpf/e:control/e:localControl/e:term')
        header['state'] = ' '.join(self.get(tree, '/e:eac-cpf/e:control/e:maintenanceAgency/e:agencyName').split()[4:])
        header['title'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:nameEntry[1]/e:part[1]')
        header['binomial_title'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:nameEntry/e:part[2]')
        header['from'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:fromDate', attrib='standardDate')
        header['from'] = header['from'].split('-')[0]
        header['to'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:toDate', attrib='standardDate')
        header['to'] = header['to'].split('-')[0]
        return header

    def get_summary(self, tree):
        """ Construct dict of the summary for the focus entity

        @params:
        tree: the etree tree to process
        """
        summary = {}
        summary['from'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:fromDate')
        summary['to'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:toDate')

        categories = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:functions/e:function/e:term')
        if type(categories) == list:
            summary['categories'] = (', ').join(self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:functions/e:function/e:term'))
        else:
            summary['categories'] = categories

        altnames = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:nameEntry[position()>1]/e:part', element=True)
        summary['altnames'] = [ n.text for n in altnames ]
        summary_note = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist/e:abstract', element=True)
        summary['summary_note'] = [ etree.tostring(f, method='html') for f in summary_note ]
        #full_note = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist/e:p', element=True)
        full_note = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist', element=True)[0]
        try:
            chronList = self.get(full_note, '//e:chronList', element=True)[0]
            full_note.remove(chronList)
        except:
            pass
        for c in full_note.getchildren():
            if c.tag == '{urn:isbn:1-931666-33-4}abstract':
                c.getparent().remove(c)
        full_note = [ etree.tostring(f, method='html') for f in full_note ]
        fn = []
        for c in full_note:
            c = c.replace('<list',  '<ul' )
            c = c.replace('</list', '</ul')
            c = c.replace('<item',  '<li' )
            c = c.replace('</item', '</li')
            fn.append(c)
        summary['full_note'] = fn

        summary['relations_earlier'] = self.get_relations_earlier(tree)
        summary['relations_later'] = self.get_relations_later(tree)
        summary['reference_document'] = self.chomp_domain(self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:entityId[1]'))
        summary['last_updated'] = self.get_last_update(tree)
        #summary['cite_this'] = self.get_guide_url(self.get(tree, '/e:eac-cpf/e:control/e:recordId'), summary['reference_document'])
        summary['cite_this'] = "%s" % self.request.url
        summary['data_feed'] = "%s/json" % self.request.url 

        keystone_element = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:resourceRelation[@resourceRelationType="other"]/e:descriptiveNote', element=True)
        summary['keystone_image_url'] = None
        summary['keystone_image'] = None
        summary['keystone_citation'] = ''
        if len(keystone_element) != 0:
            for key in keystone_element:
                if self.get(key, 'e:p') == 'Include in Gallery':
                    href = key.getparent().attrib['{http://www.w3.org/1999/xlink}href']
                    try:
                        ktree = etree.parse(href, etree.HTMLParser())
                        summary['keystone_image_url'] = self.chomp_domain(href)
                        keystone_image = self.get_image_source(href, self.get(ktree, '//img[@id="dothumb"]', attrib="src"))
                        summary['keystone_image'] = self.chomp_domain(keystone_image)

                        keystone_cite_name = self.get(key.getparent(), 'e:relationEntry')
                        keystone_cite_date = self.get(key.getparent(), 'e:objectXMLWrap/f:archref/f:unitdate')
                        keystone_cite_repo = self.get(key.getparent(), 'e:objectXMLWrap/f:archref/f:repository')
                        if len(keystone_cite_date) == 0 and len(keystone_cite_repo) == 0:
                            summary['keystone_citation'] = "%s" % keystone_cite_name
                        elif len(keystone_cite_date) == 0:
                            summary['keystone_citation'] = "%s, courtesy of %s." % (keystone_cite_name, keystone_cite_repo)
                        else:
                            summary['keystone_citation'] = "%s, %s, courtesy of %s." % (keystone_cite_name, keystone_cite_date, keystone_cite_repo)
                    except IOError:
                        log.error("get_summary: Couldn't read: %s" % href)
                    
        access_conditions = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation/e:relationEntry[@localType="Access Conditions"]', element=True)
        contact_details = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation/e:relationEntry[@localType="Contact Details"]', element=True)
        summary['access_conditions'] = ''
        for e in access_conditions:
            resource = e.getparent().attrib['{http://www.w3.org/1999/xlink}href']
            try:
                tree = etree.parse(self.get_xml(resource))
                full_note = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist/e:p', element=True)
                summary['access_conditions'] = [ etree.tostring(f, method='html') for f in full_note ]
            except IOError:
                summary['access_conditions'] = []
                log.error("get_summary: Couldn't read: %s" % resource)

        summary['contact_details'] = ''
        for e in contact_details:
            resource = e.getparent().attrib['{http://www.w3.org/1999/xlink}href']
            try:
                tree = etree.parse(self.get_xml(resource))
                full_note = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist/e:p', element=True)
                summary['contact_details'] = [ etree.tostring(f, method='text') for f in full_note ]
            except IOError:
                log.error("get_summary: Couldn't read: %s" % resource)
                summary['contact_details'] = []
        return summary

    def get_last_update(self, tree):
        event = self.get(tree, '/e:eac-cpf/e:control/e:maintenanceHistory/e:maintenanceEvent/e:eventType', element=True)
        for e in event:
            if e.text == 'updated':
                standard_date = datetime.datetime.strptime(self.get(e.getparent(), 'e:eventDateTime[@standardDateTime]'), "%Y-%m-%d")
                return datetime.datetime.strftime(standard_date, "%d %B %Y")

    def get_relations_earlier(self, tree):
        """Find the earlier relation for the focus entity

        @params:
        tree: the etree tree to process
        """

        # get the reference to the referred XML document
        #resource = str(self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation[@cpfRelationType="temporal-earlier"]', 
        #    attrib="{http://www.w3.org/1999/xlink}href"))
        resource = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation[@cpfRelationType="temporal-earlier"]', element=True)
        if resource is None:
            return None

        relations = []
        for r in resource:
            relations.append(self.get_relation_data(r.attrib['{http://www.w3.org/1999/xlink}href']))

        relations = sorted(relations, key=lambda k: k['from']) 
        return relations 


    def get_relations_later(self, tree):
        """Find the later relation for the focus entity

        @params:
        tree: the etree tree to process
        """
        relation = {} 

        # get the reference to the referred XML document
        #resource = str(self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation[@cpfRelationType="temporal-later"]', 
        #    attrib="{http://www.w3.org/1999/xlink}href"))
        resource = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation[@cpfRelationType="temporal-later"]', element=True)

        if resource is None:
            return None

        relations = []
        for r in resource:
            relations.append(self.get_relation_data(r.attrib['{http://www.w3.org/1999/xlink}href']))

        relations = sorted(relations, key=lambda k: k['from']) 
        return relations 

    def get_relation_data(self, resource):
        relation = {}
        try:
            resource = self.get_xml(resource)
            tree = etree.parse(resource)
        except IOError:
            # no earlier relation found
            log.error("get_relations_earlier: Couldn't read: %s" % resource)
            return relation

        relation['id'] = self.get(tree, '/e:eac-cpf/e:control/e:recordId')
        relation['href'] = self.get_guide_url(relation['id'], resource) 
        relation['name'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:nameEntry[1]/e:part')
        try:
            relation['from'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:fromDate', 
                attrib='standardDate').split('-')[0]
        except AttributeError:
            # not all entries have dates
            relation['from'] = ''

        try:
            relation['to'] = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:toDate', 
                attrib='standardDate').split('-')[0]
        except AttributeError:
            # not all entries have dates
            relation['to'] = ''

        return relation

    def get_glossary_terms(self, tree):
        """ Construct an array of glossary terms for the focus entity

        @params:
        tree: the etree tree to process
        """
        terms = []
        for result in self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation/e:relationEntry[@localType="Glossary Term"]', element=True):
            term = {}
            term['name'] = result.text.strip()
            term['href'] = result.getparent().attrib['{http://www.w3.org/1999/xlink}href']
            try:
            	tree = etree.parse(self.get_xml(term['href']))
                term['id'] = self.get(tree, '/e:eac-cpf/e:control/e:recordId')
                term['href'] = self.get_guide_url(term['id'], term['href'])
            except IOError:
                log.error("get_glossary_terms: Couldn't read: %s" % term['href'])
                pass
            terms.append(term)
        return terms

    def get_images(self, tree):
        """ Construct an array of images for the focus entity

        @params:
        tree: the etree tree to process
        """
        images = []
        for result in self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:resourceRelation/e:relationEntry[@localType="digitalObject"]', element=True):
            image = {}
            dobject_page = result.getparent().attrib['{http://www.w3.org/1999/xlink}href']
            image['dobject_page'] = self.chomp_domain(dobject_page)
            image['title'] = result.text

            try:
                tree = etree.parse(dobject_page, etree.HTMLParser())
                image['dobject'] = self.chomp_domain(self.get_image_source(dobject_page, self.get(tree, '//img[@id="dothumb"]', attrib="src")))
            except IOError:
                log.error("get_images: Couldn't read: %s" % dobject_page)
                image['dobject'] = ''
            images.append(image)

        # and now split the array into rows of 4
        imgs = []
        for i in  self.chunker(images, 4):
            imgs.append(i)
        return imgs

    def get_locations(self, tree):
        """ Construct an array of locations for the focus entity

        @params:
        tree: the etree tree to process
        """
        locations = []
        for result in list(self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist/e:chronList/e:chronItem', element=True)):
            location = {}
            location['title'] = self.get(result, 'e:event')
            try:
                location['from'] = self.get(result, 'e:dateRange/e:fromDate')
            except AttributeError:
                location['from'] = ''
            try:
                location['to'] = self.get(result, 'e:dateRange/e:toDate')
            except AttributeError:
                location['to'] = ''
            locations.append(location)
        return locations

    def get_records(self, tree):
        """Construct an array of records for the focus entity

        @params:
        tree: the etree tree to process
        """
        records = []  
        things = [ 'Archival Collection', 'Archival Series', 'Archival Item' ]
        for element in self.get(tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation/e:relationEntry' , element=True):
            if element.attrib['localType'] in things:
                record = {}
                record['title'] = element.text.strip()
                record['link'] = element.getparent().attrib['{http://www.w3.org/1999/xlink}href']

                # read the XML data of the linked content
                try:
                    resource = self.get_xml(record['link'])
                    ref_tree = etree.parse(self.get_xml(record['link']))
                except IOError:
                    log.error("get_records: Couldn't read: %s" % resource)
                    continue
                record['abstract'] = self.get(ref_tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist/e:abstract')
                record['id'] = self.get(ref_tree, '/e:eac-cpf/e:control/e:recordId')
                record['link'] = self.get_guide_url(record['id'], record['link'])
                record['from_date'] = self.get(ref_tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:fromDate', attrib='standardDate').split('-')[0]
                record['to_date'] = self.get(ref_tree, '/e:eac-cpf/e:cpfDescription/e:description/e:existDates/e:dateRange/e:toDate', attrib='standardDate').split('-')[0]
                record['contact_details'] = ''
                record['type'] = element.attrib['localType'].split()[1]
                record['local_type'] = self.get(ref_tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:entityId[2]', attrib='localType')
                record['reference'] = self.get(ref_tree, '/e:eac-cpf/e:cpfDescription/e:identity/e:entityId[2]')
                if record['reference'] == '':
                    record['reference'] = '-'

                contact_details = self.get(ref_tree, '/e:eac-cpf/e:cpfDescription/e:relations/e:cpfRelation/e:relationEntry[@localType="Contact Details"]', element=True)
                for e in contact_details:
                    resource = e.getparent().attrib['{http://www.w3.org/1999/xlink}href']
                    try:
                        tree = etree.parse(self.get_xml(resource))
                        full_note = self.get(tree, '/e:eac-cpf/e:cpfDescription/e:description/e:biogHist/e:p', element=True)
                        record['contact_details'] = [ etree.tostring(f, method='text') for f in full_note ]
                    except IOError:
                        log.error("get_records: Couldn't read: %s" % resource)
                records.append(record)
        return records  

    def get_image_source(self, parent_url, image_path):
        """Return the fully qualified path to an image

        @params:
        parent_url: the dobject page for the image
        image_path: the src attribute of the image
        """
        if type(image_path) != str:
            return ''
        return parent_url.split('objects')[0] + 'objects' + image_path.split('objects')[1]

    def chunker(self, seq, size):
        """Given a list, seq, return a list of lists "size" long

        @params:
        seq: the list to breakdown
        size: the number of items in each sublist
        """
        return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

    def chomp_domain(self, href):
        if 'ref' not in href:
            href = self.resolve(href)
        return href.replace("http://www.findandconnect.gov.au", "")

    def resolve(self, href):
        if 'ref' not in href:
            ref = href.replace("http://www.findandconnect.gov.au", "http://www.findandconnect.gov.au/ref")
        else:
            ref = href

        return ref.replace(self.conf.map[0], self.conf.map[1])

    def get_guide_url(self, eid, orig_href):
        """Given a document reference and entity id, return the path of that entity in the guide

        @params:
        eid: the entity id
        orig_href: the http reference of this document
        """
        state = orig_href.split('/')[4]
        try:
            state = self.state[state]
        except:
            pass

        return "/guide/%s/%s" % (state, eid)

