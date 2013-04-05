class Navigation:

    def __init__(self):
        self.nav_items = [
            {'slug':'home','text':      'Home',                 'url':'/',              'class':'',     'target':'_self'},
            {'slug':'mapper',     'text': 'Theme editor', 'url':'/mapper/',        'class':'' ,'target':'_self'},
            {'slug':'settings',    'text': 'Settings','url':'/settings/', 'class':'',     'target':'_self'},
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