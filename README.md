# README #

This is the FACP website application. What was to be the basis of the OHRM 6 rendering component.

### How do I get set up? ###

To hack on this app you'll need:

* Python 2.7, pyramid, pyramid_beaker, pyramid_debugtoolbar, Paste,pyramid_simpleform, pyramid_tm, python-ldap, webhelpers, lxml, nose, nose-cov, nose-progressive, rednose, nose_fixes

### Building a release ###

* Code in master
* Merge to testing and push to release a testing version
* Once the release is approved; merge testing in to production and push origin

On the relevant nodes, git pull then restart the application: sv restart facp-app