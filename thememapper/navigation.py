class Navigation:

    def __init__(self):
        self.nav_items = [
            {'slug':'home','text':      'Home',                 'url':'/',              'class':'',     'target':'_self'},
            {'slug':'config_editor',    'text': 'Config editor','url':'/editor/config', 'class':'',     'target':'_self'},
            {'slug':'theme_editor',     'text': 'Theme editor', 'url':'/editor',        'class':'last' ,'target':'_self'},
        ]

    def get_items(self,active='home',extra_items=None):
        import copy
        items = copy.deepcopy(self.nav_items)
        if extra_items is not None:
            items.extend(extra_items)
        for item in items:
            if item['slug'] == active:
                item['class'] += ' active'
        return items