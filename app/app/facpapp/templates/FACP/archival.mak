<%inherit file="base.mak"/>

<%block name="title">
${doc['header']['title']}
</%block>

<%block name="last_updated">
${doc['summary']['last_updated']}
</%block>

<%block name="cite_this">${doc['summary']['cite_this'] | trim}</%block>

<%block name="content">
	<div id="navtabs">
		<ul class="list-nb tabs font18">
			<li><a href="#tab1" class="btn">Summary</a></li>
            ##<li><a href="#tab2" class="btn">Sources</a></li>
			<li><a href="${doc['summary']['reference_document']}" class="btn external">Full page</a> </li>
		</ul>
		<div id='tab1'>
			<div class="entity-image">
				%if doc['summary']['keystone_image'] != None:
                <ul>
                    <li>
                        <a href="${doc['summary']['keystone_image_url']}">
                            <img src="${doc['summary']['keystone_image']}" alt="">
                        </a>
                        <p class="caption">${doc['summary']['keystone_citation']}</p>
                        <a class="details" href="${doc['summary']['keystone_image_url']}">DETAILS</a>
                    </li>
                </ul>
				%endif
			</div>
			<dl class="dl">
                %if len(doc['summary']['from']):
                    <dt>From</dt>
                    <dd>${doc['summary']['from']}</dd>
                %endif
                %if len(doc['summary']['to']):
                    <dt>To</dt>
                    <dd>${doc['summary']['to']}</dd>
                %endif
				%if len(doc['summary']['categories']):
					<dt>Categories</dt>
					<dd>${doc['summary']['categories']}</dd>
				%endif
				%if len(doc['summary']['altnames']):
					<dt>Alternative Names</dt>
					<dd>
						<ul>
							%if type(doc['summary']['altnames']) == list:
								%for name in doc['summary']['altnames']:
									<li>${name}</li>
								%endfor
							%else:
								<li>${doc['summary']['altnames']}</li>
							%endif
						</ul>
					</dd>
				%endif
				</dd>
			</dl>
			<br/>
			<p>
				%for note in doc['summary']['summary_note']:
					<p>${note | n}</p>
				%endfor
				%if len(doc['summary']['full_note']) > 0:
					<a href="#" id="fullnote_toggle">Read More</a><br/>
				%endif
			</p>

            <div class="module">
                <div id="fullnote" class="fullnote" style="display: none;">
                    <a href='#' id="fullnote_close">Less</a>
                    %if type(doc['summary']['full_note']) != list:
                        <p>${doc['summary']['full_note'] | n}</p>
                    %else:
                        %for para in doc['summary']['full_note']:
                            <p>${para | n}</p>
                        %endfor
                    %endif
                    %for note in doc['summary']['access_conditions']:
                        <p>${note | n}</p>
                    %endfor
                    ##%for note in doc['summary']['contact_details']:
                    ##	<p>${note | n}</p>
                    ##%endfor
                </div>
            </div>
            <dl class="content-summary">
                <dt>Contact</dt>
                <dd>
                %for note in doc['summary']['contact_details']:
                ${note | n}<br/>
                %endfor
                </dd>
            </dl>
		</div>
##		<div id="tab2">
##				<div id="sources" class="sources">
##				  This page was created on ${doc['header']['today']} from the following data sources:
##				  <br/>
##				  <ul>
##				  %for source in doc['sources']:
##                  <li><strong>${source['etype']}</strong>&nbsp;-&nbsp;
##                    <a href="${source['eweb']}">${source['etitle']}</a>,
##                    <small><a href="${source['esource']}" target="_blank">[view XML]</a></small>
##                  </li>
##				  %endfor
##				  </ul>
##				  The data feed for this page:&nbsp;<a href=${doc['summary']['data_feed']}>${doc['summary']['data_feed']}</a>
##				</div>
##			</div>
##			<h2>
##				Timeline
##			</h2>	
##			<dl class="dl">
##				%if len(doc['summary']['relations_earlier']) > 0:
##				<dt>${doc['summary']['relations_earlier']['from']} - ${doc['summary']['relations_earlier']['to']}</dt>
##				<dd><a href="${doc['summary']['relations_earlier']['href']}">${doc['summary']['relations_earlier']['name']}></dd>
##				%endif
##				<dt>${doc['header']['from']} - ${doc['header']['to']}</dt>
##				<dd>${doc['header']['title']}</dd>
##				%if len(doc['summary']['relations_earlier']) > 0:
##				<dt>${doc['summary']['relations_later']['from']} - ${doc['summary']['relations_later']['to']}</dt>
##				<dd><a href="${doc['summary']['relations_later']['href']}">${doc['summary']['relations_later']['name']}</a></dd>
##				%endif
##			</dl>
##		</div>
##		<div id='tab4'>
##			<dl class="entityevent">
##				%for location in doc['locations']:
##				<dt>${location['from']} - ${location['to']}</dt>
##				<dd>${location['title']}</dd>
##				%endfor
##			</dl>
##		</div>
	</div>
</%block>
