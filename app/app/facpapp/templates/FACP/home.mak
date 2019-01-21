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
			<li><a href="#tab2" class="btn">Records</a></li>
			<li><a href="#tab3" class="btn">Photos</a></li>
			##<li><a href="#tab4" class="btn">Publications</a></li>
			##<li><a href="#tab5" class="btn">Sources</a></li>
			<li><a href="${doc['summary']['reference_document']}" class="btn external">Full page</a></li>
		</ul>
		<div id='tab1'>
			<div class="entity-image">
				%if doc['summary']['keystone_image'] != None:
                <ul>
                    <li>
                        <a href="${doc['summary']['keystone_image_url']}">
                            <img src="${doc['summary']['keystone_image']}" alt="${doc['header']['title']}">
                        </a>
                        <p class="caption">
                            ${doc['summary']['keystone_citation']}
                            <br/>
                            <a class="details" href="${doc['summary']['keystone_image_url']}">DETAILS</a>
                        </p>
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
			</dl>
			<br/>
			<p>
                %for note in doc['summary']['summary_note']:
                    <p>${note | n}</p>
                %endfor
				%if len(doc['summary']['full_note']) > 0:
					<a href="#" id="fullnote_toggle">Read more</a><br/>
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
                </div>
            </div>
				<h2>
					Locations	
				</h2>	
            %if not doc['locations']:
                We do not currently have any location information recorded for this organisation.
                If you know the location of the Home please <a href="#" onclick="send('/contact/ask-us/')">contact us</a>.
            %else:
                <dl class="entityevent">
                    %for location in doc['locations']:
                    <dt>${location['from']} - ${location['to']}</dt>
                    <dd>${location['title']}</dd>
                    %endfor
                </dl>
            %endif

			%if doc['summary']['relations_earlier'] or doc['summary']['relations_later']:
                <h2>
                    Timeline
                </h2>	
                <dl class="dl">
                    %if doc['summary']['relations_earlier']:
                        %for relation in doc['summary']['relations_earlier']:
                            <dt>${relation['from']} - ${relation['to']}</dt>
                            <dd><a href="${relation['href']}">${relation['name']}</a></dd>
                         %endfor
                    %endif
                    <dt>${doc['header']['from']} - ${doc['header']['to']}</dt>
                    <dd>${doc['header']['title']}</dd>
                    %if doc['summary']['relations_later']:
                        %for relation in doc['summary']['relations_later']:
                            <dt>${relation['from']} - ${relation['to']}</dt>
                            <dd><a href="${relation['href']}">${relation['name']}</a></dd>
                         %endfor
                    %endif
                </dl>
			%endif
		</div>
		<div id='tab2'>
            <script type="text/javascript">
              function send(url) {
                window.location = url + "?u=" + encodeURIComponent(window.location) + "&t=" + encodeURIComponent(document.title);
              }
            </script>
			<div class="row row-margin-30">
				%if not doc['records']:
                    <p>
                    We do not currently have any records linked to this organisation, but records may exist.
                    The Find & Connect Support Service can help people who lived in orphanages and children's institutions look for their records.
                    </p>
                    <p>
                        You can also find out more by visiting 
                        <a href="/featured-stories/what-to-expect-when-accessing-records/#5">
                        Other important records</a>.
                    </p>
				%else:
					%for record in doc['records']:
					<div class="row module">
                        <dl class="content-summary">
                            <dt>${record['type']} Title</dt>
                            <dd>${record['title']}</dd>
                            <dt>Date Range</dt>
                            <dd>${record['from_date']} - ${record['to_date']}</dd>
                            <dt>Reference</dt>
                            <dd>
                                ${record['reference']} 
                                %if record['local_type'] != '':
                                    [${record['local_type']}]
                                %endif
                            </dd>
                            <dt>Contact</dt>
                            <dd>
                                %for note in record['contact_details']:
                                ${note | n}<br/>
                                %endfor
                                <a class="details" href="${record['link']}">DETAILS</a></a>
                            </dd>
                        </dl>
					</div>
					%endfor
				%endif
			</div>
		</div>
		<div id='tab3'>
			%if not doc['images']:
				We do not currently have any photographs linked to this organisation, but photographs may exist.
                If you know of any photographs related to this Home please <a href="#" onclick="send('/contact/ask-us/')">contact us</a>.
            %else:
				%for row in doc['images']:
					<div class="row">
						%for photo in row:
                            %if loop.index < 3:
							<div class="col">
                            %else:
							<div class="col col-last">
                            %endif
								<a href="${photo['dobject_page']}">
									<img src="${photo['dobject']}" alt="${photo['title']}">
								</a>
								<span class="caption">${photo['title']}</span>
							</div>
						%endfor
					</div>
				%endfor
			%endif
		</div>
##		<div id='tab4'>
##		</div>
##		<div id='tab5'>
##			<div id="sources" class="">
##			  This page was created on ${doc['header']['today']} from the following data sources:
##			  <br/>
##			  <ul> 
##			  %for source in doc['sources']:
##				<li><strong>${source['etype']}</strong>&nbsp;-&nbsp;
##					<a href="${source['eweb']}">${source['etitle']}</a>,
##					<small><a href="${source['esource']}" target="_blank">[view XML]</a></small>
##				</li>
##			  %endfor
##			  </ul>
##              The data feed for this page:&nbsp;<a href=${doc['summary']['data_feed']}>${doc['summary']['data_feed']}</a>
##			</div>
##		</div>
	</div>
</%block>
