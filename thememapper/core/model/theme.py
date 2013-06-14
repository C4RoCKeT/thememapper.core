import os

class _ThemeModel:
    
    def __init__(self,settings):
        self.settings = settings
    
    def get_themes(self,root_dir=None):
        if root_dir is None:
            root_dir = self.settings['themes_dir']
        themes = []
        for dirname, dirnames, filenames in os.walk(root_dir):
            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.
            if '.git' in dirnames:
                # don't go into any .git directories.
                dirnames.remove('.git')
            if filenames:
                theme = {}
                for filename in filenames:
                    basename = os.path.splitext(filename)[0]
                    if filename == 'rules.xml':
                        name = os.path.basename(dirname)
                        theme['name'] = name
                        theme['active'] = name == self.settings['theme']
                    if basename == 'preview':
                        theme['preview'] = os.path.join(dirname,filename)
                if 'name' in theme:
                    themes.append(theme)
        return themes
    
    def get_templates(self,root_dir=None):
        if root_dir is None:
            root_dir = self.settings['theme_path']
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
                            'path':os.path.join(dirname,filename),
                            'name':filename
                        })
        return templates
    
    def get_rules(self, path=None):
        if path is None:
            if os.path.isfile(self.settings['rules_path']):
                return open(self.settings['rules_path']).read()
        else:
            if os.path.isfile(path):
                return open(path).read()        
        return False
    
    def get_rule_files(self,root_dir=None):
        if root_dir is None:
            root_dir = self.settings['theme_path']
        rule_files = []
        for dirname, dirnames, filenames in os.walk(root_dir):
            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.
            if '.git' in dirnames:
                # don't go into any .git directories.
                dirnames.remove('.git')
            if filenames:
                for filename in filenames:
                    extension = os.path.splitext(filename)[1]
                    if extension == '.xml':
                        rule_files.append({
                            'path':os.path.join(dirname,filename),
                            'name':filename
                        })
        return rule_files
    
    def save_rules(self,rules,path=None):
        try:
            if path is None and os.path.isfile(self.settings['rules_path']):
                f = open(self.rules_path, "w") # This will create a new file or **overwrite an existing file**.
            elif os.path.isfile(path):
                f = open(path, "w") # This will create a new file or **overwrite an existing file**.
            else:
                return False
            try:
                f.write(rules) # Write the xml to the file
            finally:
                f.close()
                return True
        except IOError:
            return False

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