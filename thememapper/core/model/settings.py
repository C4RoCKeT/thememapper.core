import os
from ConfigParser import SafeConfigParser

class _SettingsModel:
    
    def __init__(self,path='settings.properties'):
        self.read_settings(path)
        
    def read_settings(self,path='settings.properties'):
        settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        parser = SafeConfigParser()
        # Read the Diazo paste config and set global variables
        opened_files = parser.read(settings_file)
        if opened_files:
            self.theme = parser.get('thememapper','theme')
            self.themes_dir = parser.get('thememapper','themes_directory')
            self.theme_path = os.path.join(self.themes_dir,self.theme)
            self.rules_path = os.path.join(self.theme_path,'rules.xml')
            self.content_url = parser.get('thememapper','content_url')
            self.diazo_addr = parser.get('diazo','ip')
            self.diazo_port = parser.get('diazo','port')
            self.static_path = parser.get('diazo','static')
            self.port = parser.get('thememapper','port')
            self.diazo_run = parser.get('diazo','run')
        return self.get_settings()
        
    def get_settings(self):
        return self.__dict__
        
    def save_settings(self,_post,path='settings.properties'):
        settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        parser = SafeConfigParser()
        if parser.read(settings_file):
            parser.set('thememapper','port',_post['thememapper_port'] if _post['thememapper_port'] != '' else '5001')
            parser.set('thememapper','content_url',_post['thememapper_content_url'])
            parser.set('thememapper','themes_directory',_post['thememapper_themes_directory'])
            parser.set('thememapper','theme',_post['thememapper_theme'] if 'thememapper_theme' in _post else '')
            parser.set('diazo','ip',_post['diazo_ip'] if _post['diazo_ip'] != '' else 'localhost')
            parser.set('diazo','port',_post['diazo_port'])
            parser.set('diazo','run',_post['diazo_run'] if 'diazo_run' in _post else 'False')
            parser.set('diazo','static',_post['static_path'] if 'static_path' in _post else '')
            parser.write(open(settings_file, 'wb'))
            return True
        return False