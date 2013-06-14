from flask import render_template

class _DashboardController:
    
    def __init__(self,settings):
        self.settings = settings
    
    def show_dashboard(self):
        from thememapper.core.model.theme import _ThemeModel
        themes = _ThemeModel(self.settings).get_themes()
        from thememapper.core.model.navigation import _NavigationModel
        nav_items = _NavigationModel().get_items()
        preview = False
        for theme in themes:
            if theme['active'] and 'preview' in theme:
                preview = theme['preview']
        return render_template('index.html',nav_items=nav_items,settings=self.settings,amount=len(themes),theme=self.settings['theme'],preview=preview)