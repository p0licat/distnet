
from src.tcp_file_entry import EntryTCP


from tcp_structs_exceptions import EntryTCP_FormatError

#from src.tcp_structs import C_STATE

class FileTCP(object):
    def __init__(self, path):
        self.path = path
        self.data = None
        self.entries = None
        self.removed_lines = 0

        if type(path) is not str or path == "":
            raise InitializationError("Not a valid path string: ", "{0}".format(path))

    def parse_entries(self):

        if self.data == None:
            raise InitializationError("Fatal error, no data to parse.", "Tried with path: {0}".format(self.path))

        self.entries = self.data.split("\n")

        # delete non-entry lines
        while True:
            done = True
            for index in range(len(self.entries)):
                if not isinstance(self.entries[index], EntryTCP):
                    if type(self.entries[index]) is not str or len(self.entries[index]) == 0:
                        # these lines do not pass to EntryTCP constructor
                        self.removed_lines += 1
                        del self.entries[index]
                        done = False
                        break

                    try:
                        self.entries[index] = EntryTCP(self.entries[index])
                    except EntryTCP_FormatError as fe:
                        # lines with incorrect format are removed
                        self.removed_lines += 1
                        del self.entries[index]
                        done = False
                        break
            if done:
                break

    def read_tcp_struct(self, data=None):
        if data == None:
            try:
                with open(self.path, 'r') as fd:
                    self.data = fd.read()
            except IOError as ioe:
                # Errno 2 not exist
                sys.stderr.write("Error, file not accessible.\n")
        else:
            self.data = data

        if self.data == None:
            sys.stderr.write("Nothing was read...")
        else:
            self.parse_entries()

    def print_entries(self):
        for item in self.entries:
            print(str(item)) # TODO: stream tests
