<!DOCTYPE html>
<!--[if lt IE 7]><html class="lt-ie7"> <![endif]-->
<!--[if IE 7]><html class="lt-ie8"> <![endif]-->
<!--[if IE 8]><html class="lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--><html lang="en"><!--<![endif]-->
<head>
	<meta charset="utf-8">
	<title><%block name="title"></%block> - Summary | Find &amp; Connect</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="Description" lang="en" content="Description">
	<meta name="robots" content="index, follow">
	<meta name="robots" content="noodp, noydir">
	<link rel="apple-touch-icon-precomposed" sizes="144x144" href="apple-touch-icon-144x144-precomposed.png">
	<link rel="apple-touch-icon-precomposed" sizes="114x114" href="apple-touch-icon-114x114-precomposed.png">
	<link rel="apple-touch-icon-precomposed" sizes="72x72" href="apple-touch-icon-72x72-precomposed.png">
	<link rel="apple-touch-icon-precomposed" href="apple-touch-icon-precomposed.png">
	<link rel="shortcut icon" href="/favicon.ico">
	<link rel="stylesheet" href="/assets/css/print.css" media="print">
	<link rel="stylesheet" href="/assets/css/normalize.css">
	<link rel="stylesheet" href="/assets/css/base.css">
	<link rel="stylesheet" href="/assets/css/layout.css">
	<link rel="stylesheet" href="/assets/css/modules.css">
	<link rel="stylesheet" href="/assets/css/modules-buttons.css">
	<link rel="stylesheet" href="/assets/css/modules-forms.css">
	<link rel="stylesheet" href="/assets/css/modules-nav.css">
	<link rel="stylesheet" href="/assets/css/search.css">
	<script src="/assets/js/responsive-nav2.js"></script>
	<!--[if lt IE 9]>
		<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
		<script src="/assets/js/respond.min.js"></script>
	<![endif]-->
	<script src="https://code.jquery.com/jquery-1.10.2.min.js"></script>
	<script src="https://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
	<script>
		// Wait until the DOM has loaded before querying the document
        $(function() {
                $("#navtabs").tabs({

                });
                $('a.tab-ctrl').click(function(e) {
                   var tab =  this.hash.replace('#tab', '') -1;
                   $('#navtabs').tabs({active: tab});
                   e.preventDefault();
                });
                $("#navtabs li a.external").unbind('click');

				$('#fullnote_toggle').click(function(e) {
					e.preventDefault();
					$('.fullnote').toggle();
					$('#fullnote_toggle').hide();
				});
				$('#fullnote_close').click(function(e) {
					e.preventDefault();
					$('.fullnote').toggle();
					$('#fullnote_toggle').show();
				});
        });
	</script>
    <script type="text/javascript">
      function send(url) {
        window.location = url + "?u=" + encodeURIComponent(window.location) + "&t=" + encodeURIComponent(document.title);
      }
    </script>
	<script type="text/javascript">
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', 'UA-26872007-1']);
        _gaq.push(['_trackPageview']);
        (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();

		<!-- the contact us button trigger
		This constructs the URL with the required referring page information -->

   </script>
</head>
<body>
<div class="row header-outer">
	<div class="row container header" role="banner">
		<div class="header-logo">
			<a href="/"><span><img src="/assets/img/header-logo-narrow.png" alt="Find &amp; Connect"></span></a>
		</div>
		<div class="header-details">
			<span class="header-details-small">Find &amp; Connect Support Services</span><br>
			<span class="header-details-large"><strong><a class="tel" href="tel:+611800161109">1800 16 11 09</a></strong></span><br>
			<span class="header-details-small">Freecall: Monday-Friday 9am-5pm</span>		
		</div>
	</div>
</div>
<div class="row nav-outer">
	<div class="row container nav" id="nav" role="navigation">
		<ul>
			<li class="nav-home"><a href="/">Home</a></li>
			<li class="nav-about"><a href="/about/"><strong class="nav-large">ABOUT</strong> <span class="nav-small">Find &amp; Connect</span></a></li>
			<li class="nav-homes"><a href="/look-for-homes/"><span class="nav-small">Look for</span> <strong class="nav-large">HOMES</strong></a></li>
			<li class="nav-photos"><a href="/look-for-photos/"><span class="nav-small">Look for</span> <strong class="nav-large">PHOTOS</strong></a></li>
			<li class="nav-records"><a href="/information-about-records/"><span class="nav-small">Information about</span> <strong class="nav-large">RECORDS</strong></a></li>
			<li class="nav-browse"><a href="/browse/"><strong class="nav-large">SEARCH </strong> <span class="nav-small">this site</span></a></li>
			<li class="nav-contact"><a href="/contact/"><strong class="nav-large">CONTACT</strong> <span class="nav-small">Support Services</span></a></li>
		</ul>
	</div>
</div>
<div class="row main-outer">
	<div class="row container main">
		<div class="section">
			<div class="notice">
				Some people may find content on this website distressing. <a href="/content-warning/">Read more</a>
			</div>
            <div id="state">
                ${doc['header']['state']} - ${doc['header']['localtype']}
            </div>
            <h1 style="margin-bottom: 5px;">
                ${doc['header']['title']}&nbsp;(${doc['header']['from']}&nbsp;-&nbsp;${doc['header']['to']})
            </h1>
            %if doc['header']['title'] != '':
            <div class="subname" style="margin-bottom: 10px;">
                ${doc['header']['binomial_title']}
            </div>
            %endif
            <!-- CONTENT -->
            <%block name="content">
            </%block>

		</div>
		<div class="aside" role="complementary">
			<div class="dots">
				<a class="question" href="#" onclick="send('/contact/support-service/')">
					Send message to
				    <strong>Find & Connect support service</strong>
                </a>
			</div>
##			<div class="dots">
##				<h3>
##					Look for similar
##				</h3>
##				<ul class="list-bullet">
##					<li><a href="#">Children's Home</a></li>
##					<li><a href="#">Home</a></li>
##					<li><a href="#">Protestant</a></li>
##					<li><a href="#">Reformatory</a></li>
##					<li><a href="#">Salvation Army</a></li>
##					<li><a href="#">Youth Training Centre</a></li>
##				</ul>
##			</div>
			%if doc['glossary']:
				<div class="dots">
					<h3>
						Find out what these words mean
					</h3>
					<ul class="list-bullet">
						%for entry in doc['glossary']:
							<li><a href="${entry['href']}">${entry['name']}</a></li>
						%endfor
					</ul>
				</div>
			%endif
		</div>
	</div>
</div>
<div class="row footer-rich-outer">
	<div class="row container footer-rich">
		<div class="col">
            <h4 class="mbs">About</h4>
			<ul class="list-bullet">
				<li><a href="/about/">About Find &amp; Connect</a></li>
				<li><a href="/about/acknowledgement/">Acknowledgement</a></li>
				<li><a href="/about/background/">Background</a></li>
				<li><a href="/about/accessibility/">Accessibility</a></li>
				<li><a href="/about/web-resource-credits/">Credits</a></li>
				<li><a href="/about/feedback/">Feedback</a></li>
				<li><a href="/about/content-warning/">Content Warning</a></li>
				<li><a href="/about/terms-and-conditions/">Terms &amp; Conditions</a></li>
                <li><a href="/help/factsheet-1-how-to-use-the-website/">How to use this Site</a></li>
                <li><a href="/help/faqs/">Frequently Asked Questions (FAQs)</a></li>
			</ul>
		</div>
		<div class="col">
			<h4 class="mbs">Information about Records</h4>
			<ul class="list-bullet">
				<li><a href="/resources/where-to-start/">Where to Start</a></li>
				<li><a href="/resources/family-tracing/">Family Tracing</a></li>
				<li><a href="/resources/former-child-migrants/">Former Child Migrants</a></li>
				<li><a href="/resources/stolen-generations/">Stolen Generations</a></li>
				<li><a href="/resources/what-to-expect-when-accessing-records/">What to Expect when Accessing Records about You</a></li>
				<li><a href="/resources/historical-background-about-child-welfare/">Historical Background About Child Welfare</a></li>
				<li><a href="/resources/searching-for-records-of-a-parent-or-grandparent/">Searching for Records of a Parent or Grandparent</a></li>
				<li><a href="/resources/your-rights/">Applying for Records: Your Rights and the Law</a></li>
				<li><a href="/resources/disability-homes/">Disability Homes</a></li>
				<li><a href="/resources/records-from-salvation-army-homes/">Salvation Army Homes</a></li>
				<li><a href="/resources/adoptions/">Adoptions</a></li>
				<li><a href="/resources/family-history/">Family History</a></li>
			</ul>
		</div>
		<div class="col">
			<h4 class="mbs">Featured Stories</h4>
			<ul class="list-bullet">
			<li><a href="/featured-stories/timeline-interactive/">Child Welfare Timeline</a></li>
			</ul>
			<br/>
			<h4 class="mbs">Resources</h4>
			<ul class="list-bullet">
				<li><a href="/resources/radp/">Resources for Record Holders</a></li>
				<li><a href="/resources/find-connect-web-resource-induction-pack/">Find &amp Connect web resource Induction Pack</a></li>
			</ul>
		</div>
		<div class="col col-last">
			<h4 class="mbs mt">Connect</h4>
			<ul class="list-social">
                <li class="list-social-twitter"><a href="https://twitter.com/FaCWebResource" target="_blank">Twitter</a></li>
                <li class="list-social-youtube"><a href="https://www.youtube.com/user/FindandConnect" target="_blank">YouTube</a></li>
                <li class="list-social-blog"><a href="http://www.findandconnectwrblog.info" target="_blank">Blog</a></li>
                <li class="list-social-support-services"><a href="/contact/">Support Services</a></li>
            </ul>
		</div>
	</div>
</div>
<div class="row footer-outer">
	<div class="row container footer" role="contentinfo">
		<div class="section-home">
			<p>
				<img src="/assets/img/footer-logo.png" alt="Find &amp; Connect">
			</p>
			<p class="font13">
				Last updated: <%block name="last_updated"></%block><br/>
				Cite this: <%block name="cite_this"></%block><br>
				First published by the Find &amp; Connect Web Resource Project for the Commonwealth of Australia, 2011
			</p>
		</div>
		<div class="aside-home">
			<p class="cc-logo">
				<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/au/"><img src="/assets/img/by-nc-sa.png" alt="Creative commons"></a>
			</p>
			<p class="font13 cc-text">
				Except where otherwise noted, content on this site is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/au/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>
			</p>
		</div>
	</div>
</div>
	<script type="text/javascript">
		try {
		  var navigation = responsiveNav("nav", {label: "Site menu"});
		} catch (e) { }
		try {
			var subnav = responsiveNav("subnav", {label: "Section menu"});
		} catch (e) { }
	</script>
</body>
</html>
