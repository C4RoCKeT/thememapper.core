from flask import Flask,request
from flask import render_template,Response
from flask import abort
from werkzeug.routing import BaseConverter
import optparse
import os
import sys
from navigation import Navigation
from mapper import Mapper

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.debug = True

app.url_map.converters['regex'] = RegexConverter

def main():
    global nav
    global mapper
    
    #initialize the necessary classes
    nav = Navigation()
    mapper = Mapper(get_settings())
    # Adds the ability to set config file and port through commandline
    p = optparse.OptionParser()
    p.add_option('--ip', '-i', default=mapper.ip)
    p.add_option('--port', '-p', default=mapper.port)
    options = p.parse_args()[0]
    port = options.port
    ip = options.ip
    
    #start thememapper
    app.run(str(ip), int(port),extra_files=[os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "settings.properties")])

@app.route("/")
def index():
    themes = mapper.get_themes()
    amount= len(themes)
    preview = False
    for theme in themes:
        if theme['active'] and 'preview' in theme:
            preview = theme['preview']
    return render_template('index.html',nav_items=nav.get_items(),mapper=mapper,amount=amount,theme=mapper.theme,preview=preview)

@app.route("/mapper/", methods=["GET", "POST"])
@app.route("/mapper/<name>/", methods=["GET", "POST"])
def mapper(name=None):
    if name is None:
        if request.method == 'POST':
            mapper.save_rules(request.form['rules'])
        # append the navigation with extra items
        extra_items = [
            {'text': 'Generate rule',       'slug':'',  'url':'Javascript:void(0);',    'class':'extra theme-mapper-generate','target':'_self'},
            {'text': 'View themed website', 'slug':'',  'url':mapper.themed_url,               'class':'extra',                     'target':'_blank'}
        ]
        return render_template('mapper/index.html',nav_items=nav.get_items('theme_mapper',extra_items),mapper=mapper)
    return render_template('mapper/' + name + '.html',nav_items=nav.get_items('theme_mapper'))

@app.route("/settings/", methods=["GET", "POST"])
@app.route("/settings/<name>/", methods=["GET", "POST"])
def settings(name=None):
    if name is None:
        if request.method == 'POST':
            save_settings(request.form)
            mapper.reload(get_settings())
        return render_template('settings/index.html',nav_items=nav.get_items('settings'),settings=get_settings(),mapper=mapper)
    return render_template('mapper/' + name + '.html',nav_items=nav.get_items('settings'))


@app.route("/mapper/iframe/<name>/")
@app.route('/mapper/iframe/<name>/<regex("(.*)"):filename>')
def iframe(name=None,filename='index.html'):
    if name is not None:
        if name == 'theme':
            # Only local themes are supported right now.
            import mimetypes
            mimetypes.init()
            path = os.path.join(mapper.theme_path,"/" + filename)
            # Check the file exists; if so, open it, return it with the correct mimetype.
            if os.path.isfile(path):
                return Response(file(path), direct_passthrough=True,mimetype=mimetypes.types_map[os.path.splitext(path)[1]])
            else:
                abort(404)
        else:
            #use the requests library to get the content of the content website
            import requests
            r = requests.get(mapper.content_url)
            return render_template('mapper/iframe-safe.html',url=mapper.content_url,content=r.text)
    abort(404)
    
def get_settings(config=False,path='settings.properties'):
    from ConfigParser import SafeConfigParser
    settings_file = os.path.join(os.path.dirname(__file__), path)
    parser = SafeConfigParser()
    # Read the Diazo paste config and set global variables
    opened_files = parser.read(settings_file)
    if opened_files:
        if config:
            return parser
        settings = {
            'thememapper_ip':parser.get('thememapper','ip'),
            'thememapper_port':parser.get('thememapper','port'),
            'thememapper_content_url':parser.get('thememapper','content_url'),
            'thememapper_themes_directory':parser.get('thememapper','themes_directory'),
            'thememapper_theme':parser.get('thememapper','theme'),
            'diazo_ip':parser.get('diazo','ip'),
            'diazo_port':parser.get('diazo','port'),
        }
    else:
        settings = False
    return settings

def save_settings(settings,path='settings.properties'):
    global mapper
    parser = get_settings(True)
    parser.set('thememapper','ip',settings['thememapper_ip'])
    parser.set('thememapper','port',settings['thememapper_port'])
    parser.set('thememapper','content_url',settings['thememapper_content_url'])
    parser.set('thememapper','themes_directory',settings['thememapper_themes_directory'])
    parser.set('thememapper','theme',settings['thememapper_theme'] if 'thememapper_theme' in settings else '')
    parser.set('diazo','ip',settings['diazo_ip'])
    parser.set('diazo','port',settings['diazo_port'])
    with open(os.path.join(os.path.dirname(__file__), path), 'wb') as settings_file:
        parser.write(settings_file)
    

if __name__ == "__main__":
    main()