ThemeMapper for Diazo
=====

This is a theme editor for Diazo. This theme editor differs from the one found in Plone; it is a stand-alone theme editor. It does require Diazo of course!

Quickstart
=====

I presume there is already a Diazo instance running. If not, go to http://docs.diazo.org/en/latest/quickstart.html for a quickstart.

When you (already) have your Diazo instance up and running navigate to the root of ThemeMapper.
Now edit the "paste_config_path" variable found in /thememapper/config.py::

    paste_config_path = "/path/to/paste/config.ini" # the Diazo paste config. "proxy.ini" if you followed the quickstart

Navigate to root of ThemeMapper and execute the following command to start it.

    $ python thememapper/thememapper.py

Alternatively you can start the server by calling

    $ python thememapper/thememapper.py --port 5001 --config "/path/to/paste/config.ini"

Install and configure ThemeMapper
=====

TODO
