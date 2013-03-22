ThemeMapper for Diazo
=====

This is a theme editor for Diazo. This theme editor differs from the one found in Plone; it is a stand-alone theme editor. It does require Diazo of course!

It is still a work in progress. No file browser, no support for external webpages / themes. If something works; awesome. If it doesn't; to bad.

Quickstart
=====

I presume there is already a Diazo instance running. If not, go to http://docs.diazo.org/en/latest/quickstart.html for a quickstart.

When you (already) have your Diazo instance up and running navigate to the root of ThemeMapper.
Now edit the "paste_config_path" variable found in /thememapper/config.py::

    paste_config_path = "/path/to/paste/config.ini" # the Diazo paste config. "proxy.ini" if you followed the quickstart

Before running Thememapper you must also have Flask and libcurl installed.

http://flask.pocoo.org/docs/installation/

And

https://pypi.python.org/pypi/pycurl

Once you have those installed, navigate to the root of ThemeMapper and execute the following command to start it.

    $ python thememapper/thememapper.py

Alternatively you can start the server by calling

    $ python thememapper/thememapper.py --port 5001 --config "/path/to/paste/config.ini"

ThemeMapper will read your paste config and use the values found in there.
It will use:: 

    [filter:theme]
    rules = /path/to/themes/directory/basic/rules.xml

    [app:content]
    address = http://localhost/

The rules path will be used for the rules.xml, but it will be also used for the theme directory (strips rules.xml).
The address will be the content url. You could use an external address here, but I don't give a guarantee it will work.

ThemeMapper requirements
=====

There aren't any real requirements. You can run ThemeMapper as a standalone application. Though you might find it useful to
run a Diazo instance and specify the Diazo address in the settings. That way you can preview your mappings.