import os

class Mapper:

    def __init__(self,rules_path):
        self.rules_path = rules_path

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

    def get_file_tree(self,root_dir):
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

    def get_templates(self,root_dir):
        tree = []
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
                        tree.append({
                        'path':dirname + '/' + filename,
                        'name':filename
                        })
        return tree
