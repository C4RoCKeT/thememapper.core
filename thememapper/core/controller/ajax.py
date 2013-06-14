from flask import Response,abort

class _AjaxController:
    
    def __init__(self,settings):
        self.settings = settings
    
    def abort(self,error_code):
        abort(error_code)
        
    def get_rules(self,_post):
        from thememapper.core.model.theme import _ThemeModel
        rules = _ThemeModel(self.settings).get_rules(_post['path'])
        return Response(rules,mimetype='application/xml')
    
    def save_rules(self,_post):
        from thememapper.core.model.theme import _ThemeModel
        if _ThemeModel(self.settings).save_rules(_post['rules'],_post['path']):
            return 'Rules saved', 200
        abort(404)