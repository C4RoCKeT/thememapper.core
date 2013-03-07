from flask import Flask,request
from flask import render_template,Response
from flask import abort
from werkzeug.routing import BaseConverter
import optparse
import os
import config
from navigation import Navigation
from editor import Editor

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
    global editor

    # Adds the ability to set config file and port through commandline
    p = optparse.OptionParser()
    p.add_option('--config', '-c', default=config.paste_config_path)
    p.add_option('--port', '-p', default=5001)
    options = p.parse_args()[0]
    paste_config_path = options.config
    port = options.port

    #reload if these files change
    extra_files = [paste_config_path]
    
    # Read the Diazo paste config and set global variables
    from ConfigParser import SafeConfigParser
    parser = SafeConfigParser()
    parser.read(paste_config_path)
    content_url = parser.get('app:content','address')
    rules_path = parser.get('filter:theme','rules')
    themed_url = 'http://' + parser.get('server:main','host') + ':' + parser.get('server:main','port')
    theme_path = os.path.dirname(rules_path)
    parser.write(open(paste_config_path, 'w'))

    nav = Navigation()
    editor = Editor(rules_path)

    run(port,extra_files)

def run(port,extra_files):
    # Start the server
    app.run('0.0.0.0', int(port),extra_files=extra_files)

@app.route("/")
def index():
    return render_template('index.html',nav_items=nav.get_items())

@app.route("/editor/", methods=["GET", "POST"])
@app.route("/editor/<name>/", methods=["GET", "POST"])
def editor(name=None):
    if name is None:
        if request.method == 'POST':
            editor.save_rules(request.form['rules'])
        rules_xml = editor.get_rules()
        file_tree = editor.get_file_tree(theme_path);
        templates = editor.get_templates(theme_path);
        vars = {
            'theme_path':theme_path,
            'content_url':content_url,
            'rules_xml':rules_xml,
            'tree':file_tree,
            'templates':templates
        }
        # append the navigation with extra items
        extra_items = [
            {'text': 'Generate rule',       'slug':'',  'url':'Javascript:void(0);',    'class':''},
            {'text': 'View themed website', 'slug':'',  'url':themed_url,               'class':''}
        ]
        return render_template('editor/index.html',nav_items=nav.get_items('theme_editor',extra_items),editor=vars)
    elif name == 'config':
        if request.method == 'POST':
            paste_config = request.form['paste_config']
            try:
                f = open(paste_config_path, "w") # This will create a new file or **overwrite an existing file**.
                try:
                    f.write(paste_config) # Write the paste config
                finally:
                    f.close()
            except IOError:
               pass
        return render_template('editor/' + name + '.html',nav_items=nav.get_items('config_editor'), paste_config=open(paste_config_path).read())
    return render_template('editor/' + name + '.html',nav_items=nav)

@app.route("/editor/iframe/<name>/")
@app.route("/editor/iframe/<name>/<filename>")
@app.route('/editor/iframe/<name>/<regex("(.*/)([^/]*)"):filename>')
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
            return render_template('editor/iframe-safe.html',url=url,content=content)
    abort(404)

if __name__ == "__main__":
    main()