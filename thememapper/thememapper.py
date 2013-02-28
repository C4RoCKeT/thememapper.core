from flask import Flask,url_for,redirect,request
from flask import render_template,Response
from flask import abort
from werkzeug.routing import BaseConverter
import optparse
import os
import config

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.debug = True

app.url_map.converters['regex'] = RegexConverter

def main():
    global content_url,theme_path,rules_path,paste_config_path,themed_url

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
    themed_url = parser.get('server:main','host') + ':' + parser.get('server:main','port')
    theme_path = os.path.dirname(rules_path)
    parser.write(open(paste_config_path, 'w'))
    run(port,extra_files)

def run(port,extra_files):
    # Start the server
    app.run('0.0.0.0', int(port),extra_files=extra_files)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/editor/theme/files/")
def files():
    tree = {}
    rootDir = theme_path
    for dirName, subdirList, fileList in os.walk(rootDir):
        found_files = []
        print subdirList
        if subdirList:
            for subdir in subdirList:
                found_files.append({'name':subdir,'type':folder})
        for fname in fileList:
            if fname[-1:] != '~':
                found_files.append(fname)
        tree[dirName] = found_files
    if tree:
        return render_template('editor/file-tree.html',tree=tree)
    abort(404)

@app.route("/editor/", methods=["GET", "POST"])
@app.route("/editor/<name>/", methods=["GET", "POST"])
def editor(name=None):
    if name is None:
        if request.method == 'POST':
            try:
                f = open(rules_path, "w") # This will create a new file or **overwrite an existing file**.
                try:
                    f.write(request.form['rules']) # Write the xml to the file
                finally:
                    f.close()
            except IOError:
                pass
        rules_xml = open(rules_path).read()
        return render_template('editor/index.html',theme_path=theme_path,content_url=content_url,rules_xml=rules_xml,themed_url=themed_url)
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
        return render_template('editor/' + name + '.html', name=name, paste_config=open(paste_config_path).read())
    return render_template('editor/' + name + '.html', name=name)

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

@app.route("/login/", methods=["GET", "POST"])
def login():
    return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    #logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    main()