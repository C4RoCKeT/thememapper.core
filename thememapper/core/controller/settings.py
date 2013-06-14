from thememapper.core.model.settings import _SettingsModel
from flask import render_template,redirect

class _SettingsController:
    
    def __init__(self):
        self.settings_model = _SettingsModel()
        self.settings = self.settings_model.get_settings()
    
    def show_settings(self,name='index'):
        from thememapper.core.model.navigation import _NavigationModel
        from thememapper.core.model.theme import _ThemeModel
        nav = _NavigationModel()
        themes = _ThemeModel(self.settings)
        return render_template('settings/' + name + '.html',nav_items=nav.get_items('settings'),settings=self.settings,themes=themes.get_themes())
    
    def save_settings(self,_post):
        old_port = self.settings['port']
        if self.settings_model.save_settings(_post):
            self.settings = self.settings_model.read_settings()
        if old_port != self.settings['port']:
            return redirect('http://localhost:' + self.settings['port'] + '/settings/')
        return False