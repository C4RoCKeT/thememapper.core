from flask import render_template

class _EditorController:
    
    def __init__(self,settings):
        self.settings = settings
    
    def show_editor(self,name):
        from thememapper.core.model.navigation import _NavigationModel
        nav_items = _NavigationModel().get_items('editor')
        from thememapper.core.model.theme import _ThemeModel
        theme_model = _ThemeModel(self.settings)
        rules = theme_model.get_rules()
        rule_files = theme_model.get_rule_files()
        templates = theme_model.get_templates()
        if name is None:
            return render_template('editor/index.html',nav_items=nav_items,settings=self.settings,rules=rules,rule_files=rule_files,templates=templates)
        return render_template('editor/' + name + '.html',nav_items=nav_items)
    
    def show_result(self,path):
        from urlparse import urlparse,urljoin
        if path == '' or path is None:
            path = self.settings['content_url']
        result_url = urljoin('http://' + self.settings['diazo_addr'] + ':' + self.settings['diazo_port'],urlparse(path).path)
        return render_template('editor/result-safe.html',result_url=result_url)