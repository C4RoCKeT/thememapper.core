ThemeMapper for Diazo
=====

This is a theme editor for Diazo. This theme editor differs from the one found in Plone; it is a stand-alone application. It does require Diazo to apply the XML ofc!

It is still a work in progress. No file browser, no support for external webpages / themes. If something works; awesome. If it doesn't; too bad.

Installation
=====

I presume there is already a Diazo instance running. If not, go to http://docs.diazo.org/en/latest/quickstart.html for a quickstart.

Good, when you have a Diazo server running you are ready to proceed to the next step.

To install of GitHub:: 

    $ pip install -e git+git://github.com/C4RoCKeT/thememapper.core.git#egg=thememapper.core
    
Not yet supported:
    
To install of Pypi:: 

    $ pip install thememapper.core

And to run thememapper.core:: 

    $ thememapper

ThemeMapper requirements
=====

There aren't any real requirements. You can run ThemeMapper as a standalone application. Though you might find it useful to
run a Diazo instance and specify the Diazo address in the settings. That way you can preview your mappings.