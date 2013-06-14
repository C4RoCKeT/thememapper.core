from thememapper.core.model.settings import _SettingsModel
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload


class _ServerController:
    
    def __init__(self,app,args=None):
        self.settings_model = _SettingsModel()
        self.settings = self.settings_model.get_settings()
        if args:
            for key, value in args.__dict__.iteritems():
                if value:
                    self.settings[key] = value
        print "Starting thememapper on http://0.0.0.0:" + self.settings['port']
        HTTPServer(WSGIContainer(app)).listen(self.settings['port'])
        if self.settings['diazo_run'] == 'True':
            try: 
                from thememapper.diazo import server
                print "Starting diazo on http://0.0.0.0:" + self.settings['diazo_port']
                HTTPServer(server.get_application(self.settings)).listen(self.settings['diazo_port'])
            except ImportError: 
                print "You will need to install thememapper.diazo before being able to use this function."
                
    def reload(self):
        print "===== auto-reloading ====="
        
    def start(self):
        ioloop = IOLoop.instance()
        autoreload.add_reload_hook(self.reload)
        autoreload.start(ioloop)
        ioloop.start()
        
    def watch(self,file = None):
        if file is not None:
            autoreload.watch(file)