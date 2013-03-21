import os

class Mapper:
    def __init__(self,settings):
        self.reload(settings)
        
    
    def reload(cls,settings):
        cls.theme = settings['thememapper_theme']
        cls.themes_dir = settings['thememapper_themes_directory']
        cls.theme_path = os.path.join(cls.themes_dir,cls.theme)
        cls.rules_path = os.path.join(cls.theme_path,'rules.xml')
        cls.content_url = settings['thememapper_content_url']
        cls.themed_url = 'http://' + settings['diazo_ip'] + ':' + settings['diazo_port']
        cls.ip = settings['thememapper_ip']
        cls.port = settings['thememapper_port']
        
    
    def save_rules(self,rules):
        try:
            f = open(self.rules_path, "w") # This will create a new file or **overwrite an existing file**.
            try:
                f.write(rules) # Write the xml to the file
            finally:
                f.close()
        except IOError:
            pass

    def get_rules(self):
        return open(self.rules_path).read()

    def get_file_tree(self,root_dir=None):
        if root_dir is None:
            root_dir = self.themes_dir
        tree = {}
        for dirname, dirnames, filenames in os.walk(root_dir):
            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.
            if '.git' in dirnames:
                # don't go into any .git directories.
                dirnames.remove('.git')
            # print path to all subdirectories first.
            for subdirname in dirnames:
                tree[os.path.join(dirname, subdirname)] = []
            if filenames:
                 tree[dirname] = filenames
        return tree

    def get_templates(self,root_dir=None):
        if root_dir is None:
            root_dir = self.theme_path
        templates = []
        for dirname, dirnames, filenames in os.walk(root_dir):
            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.
            if '.git' in dirnames:
                # don't go into any .git directories.
                dirnames.remove('.git')
            if filenames:
                for filename in filenames:
                    extension = os.path.splitext(filename)[1]
                    if extension == '.html' or extension == '.htm':
                        templates.append({
                        'path':dirname + '/' + filename,
                        'name':filename
                        })
        return templates
    
    def get_themes(self,root_dir=None):
        if root_dir is None:
            root_dir = self.themes_dir
        themes = []
        for dirname, dirnames, filenames in os.walk(root_dir):
            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.
            if '.git' in dirnames:
                # don't go into any .git directories.
                dirnames.remove('.git')
            if filenames:
                for filename in filenames:
                    if filename == 'rules.xml':
                        name = os.path.basename(dirname)
                        print name + "==" + self.theme + "\n\r"
                        themes.append({
                        'name':name,
                        'active':True if name == self.theme else False
                        })
        return themes
