import os
from flask import render_template,abort,Response

class _IframeController:
    
    def __init__(self,settings):
        self.settings = settings
    
    def show_iframe(self,name,path=''):
        if name is not None:
            if name == 'theme':
                # Only local themes are supported right now.
                import mimetypes
                mimetypes.init()
                path = os.path.join(self.settings['theme_path'],"/" + path)
                # Check the file exists; if so, open it, return it with the correct mimetype.
                if os.path.isfile(path):
                    return Response(file(path), direct_passthrough=True,mimetype=mimetypes.types_map[os.path.splitext(path)[1]])
                else:
                    abort(404)
            else:
                if path == '':
                    path = self.settings['content_url']
                #use the requests library to get the content of the content website
                import requests
                r = requests.get(path)
                return render_template('editor/iframe-safe.html',url=path,content=r.text)
        abort(404)