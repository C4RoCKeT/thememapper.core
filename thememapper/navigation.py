class Navigation:

    def __init__(self):
        self.nav_items = [
            {'slug':'home','text':      'Home',                 'url':'/',              'class':''},
            {'slug':'config_editor',    'text': 'Config editor','url':'/editor/config', 'class':''},
            {'slug':'theme_editor',     'text': 'Theme editor', 'url':'/editor',        'class':''},
        ]

    def get_items(self,active='home',extra_items=None):
        import copy
        if extra_items is not None:
            items = copy.deepcopy(self.nav_items);
            items.extend(extra_items)
        else:
            items = self.nav_items
        for item in items:
            if item['slug'] == active:
                item['class'] += 'active'
        return items