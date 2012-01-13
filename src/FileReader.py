import os

__author__ = 'ids'


class FileReader:
    PROPERTY_FILE_NAME = 'user.properties'
    DIPLO_DIRECTORY = '.webdiplo'
    DEFAULT_KEYS = ['username', 'password', 'email']

    def __init__(self, portable = False):
        #look for config in the current working directory, if not found, create location in user home
        if portable:
            self.path = os.getcwd()
        else:
            self.path = os.path.join(os.path.expanduser('~'), self.DIPLO_DIRECTORY)
            if not os.path.isdir(self.path):
                os.mkdir(self.path)

    def write_empty_props(self, file_path):
        print 'Creating template properties file at', file_path

        file = open(file_path, 'w')
        for key in self.DEFAULT_KEYS:
            file.write(key + '=\n')

    def read_properties(self):
        file_path = os.path.join(self.path, self.PROPERTY_FILE_NAME)
        if not os.path.isfile(file_path):
            self.write_empty_props(file_path)
            return None

        print 'Using config at', file_path

        prop_file = file(file_path)
        props = {}
        for prop_line in prop_file:
            prop_def= prop_line.strip()
            if not len(prop_def):
                continue
            if prop_def[0] in ( '!', '#' ):
                continue
            punctuation= [ prop_def.find(c) for c in ':= ' ] + [ len(prop_def) ]
            found= min( [ pos for pos in punctuation if pos != -1 ] )
            name= prop_def[:found].rstrip()
            value= prop_def[found:].lstrip(":= ").rstrip()
            props[name]= value
        prop_file.close()

        for prop_key in self.DEFAULT_KEYS:
            if prop_key not in props:
                print 'Missing required property', prop_key
                return None

        return props