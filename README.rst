ThemeMapper for Diazo
=====

This is a theme editor for Diazo. This theme editor differs from the one found in Plone; it is a stand-alone application. It does require Diazo to apply the XML ofc!

It is still a work in progress. No file browser, no support for external webpages / themes. If something works; awesome. If it doesn't; too bad.

Installation
=====

To install of GitHub:: 

    $ pip install -e git+git://github.com/C4RoCKeT/thememapper.core.git#egg=thememapper.core
    
Not yet supported:
    
To install of Pypi:: 

    $ pip install thememapper.core
    
How to use
=====

After the installation you will be able to run thememapper.core through the commandline::

    $ thememapper

Thememapper.core normally listends to port 5000. You can force it to listen on another port by running::
    
    $ thememapper -p <port>
    
For more commands just run::

    $ thememapper --help
    
Themes and you!
=====

To be able to use themes with thememapper there is just one little requirement: there should be an XML file named rules.xml in the root
of the theme.

This is what a basic rules.xml should look like::

    <rules
	xmlns="http://namespaces.plone.org/diazo"
	xmlns:css="http://namespaces.plone.org/diazo/css"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<theme href="index.html" />
    </rules>
    
Of course you should have the theme href pointing at the right file. Since index.html is quite standard I used it here.

If you want to have a screenshot of your theme to be shown in thememapper.core you could place an image file named
preview.(jpg|jpeg|png|bmp|gif) in the root of the theme as well.
    
thememapper.diazo
=====

If you want to test your mapped theme and you don't have your own Diazo instance running you can install thememapper.diazo.
Thememapper.diazo is, like thememapper.core, a stand-alone application and does not require thememapper.core to run. For more information please refer to the
readme of thememapper.diazo. https://github.com/C4RoCKeT/thememapper.diazo