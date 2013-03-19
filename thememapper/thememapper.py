from flask import Flask,request
from flask import render_template,Response
from flask import abort
from werkzeug.routing import BaseConverter
import optparse
import os
import config
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
    global content_url
    global theme_path
    global paste_config_path
    global themed_url
    global nav
    global mapper

    # Adds the ability to set config file and port through commandline
    p = optparse.OptionParser()
    p.add_option('--ip', '-i', default="0.0.0.0")
    p.add_option('--port', '-p', default=5001)
    options = p.parse_args()[0]
    port = options.port
    ip = options.ip

    content_url = 'http://www.ping-win.nl/'
    rules_path = '/home/c4rocket/Documents/Projects/diazo-test/themes/dangled/rules.xml'
    themed_url = 'http://' + '127.0.0.1' + ':' + '5000'
    theme_path = os.path.dirname(rules_path)
    nav = Navigation()
    mapper = Mapper(rules_path)
    
    #start thememapper
    app.run(str(ip), int(port))

@app.route("/")
def index():
    return render_template('index.html',nav_items=nav.get_items())

@app.route("/mapper/", methods=["GET", "POST"])
@app.route("/mapper/<name>/", methods=["GET", "POST"])
def mapper(name=None):
    if name is None:
        if request.method == 'POST':
            mapper.save_rules(request.form['rules'])
        rules_xml = mapper.get_rules()
        file_tree = mapper.get_file_tree(theme_path);
        templates = mapper.get_templates(theme_path);
        vars = {
            'theme_path':theme_path,
            'content_url':content_url,
            'rules_xml':rules_xml,
            'tree':file_tree,
            'templates':templates
        }
        # append the navigation with extra items
        extra_items = [
            {'text': 'Generate rule',       'slug':'',  'url':'Javascript:void(0);',    'class':'extra theme-mapper-generate','target':'_self'},
            {'text': 'View themed website', 'slug':'',  'url':themed_url,               'class':'extra',                     'target':'_blank'}
        ]
        return render_template('mapper/index.html',nav_items=nav.get_items('theme_mapper',extra_items),mapper=vars)
    return render_template('mapper/' + name + '.html',nav_items=nav.get_items('theme_mapper'))

@app.route("/settings/", methods=["GET", "POST"])
@app.route("/settings/<name>/", methods=["GET", "POST"])
def settings(name=None):
    if name is None:
        return render_template('settings/index.html',nav_items=nav.get_items('settings'))
    return render_template('mapper/' + name + '.html',nav_items=nav.get_items('settings'))


@app.route("/mapper/iframe/<name>/")
@app.route("/mapper/iframe/<name>/<filename>")
@app.route('/mapper/iframe/<name>/<regex("(.*/)([^/]*)"):filename>')
def iframe(name=None,filename='index.html'):
    if name is not None:
        if name == 'theme':
            # Only local themes are supported right now.
            import mimetypes
            mimetypes.init()
            path = theme_path + '/' + filename
            # Check the file exists; if so, open it, return it with the correct mimetype.
            if os.path.isfile(path):
                return Response(file(path), direct_passthrough=True,mimetype=mimetypes.types_map[os.path.splitext(path)[1]])
            else:
                abort(404)
        else:
            import pycurl
            import cStringIO
            buf = cStringIO.StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, content_url)
            c.setopt(c.WRITEFUNCTION, buf.write)
            c.setopt(c.FOLLOWLOCATION, 1)
            c.setopt(c.MAXREDIRS, 10)
            c.perform()
            content = buf.getvalue()
            buf.close()
            url = content_url
            return render_template('mapper/iframe-safe.html',url=url,content=content)
    abort(404)

if __name__ == "__main__":
    main()