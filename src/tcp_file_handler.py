"""
    File parser and syntax analysis class, for /proc/net/tcp.
"""
from src.tcp_file_entry import EntryTCP
from src.tcp_structs_exceptions import  EntryTCP_Error,\
                                        EntryTCP_FormatError, \
                                        FileTCP_InitError

class FileTCP(object):
    """
        File data parser.
    """
    def __init__(self, path):
        self.path = path
        self.data = None
        self.entries = None
        self.removed_lines = 0

        if type(path) is not str or path == "":
            raise FileTCP_InitError("Not a valid path string: ", "{0}".format(path))

    def parse_entries(self):
        """
            If self.data is populated with the /net/tcp text file's read data,
            it is analyzed by parse_entries for syntax checking, and passing
            lines will be converted into EntryTCP objects and stored in object
            self.entries.
        """
        if self.data is None:
            raise FileTCP_InitError("Fatal error, no data to parse.", "Tried with path: {0}".format(self.path))

        self.entries = self.data.split("\n")

        # delete non-entry lines
        while True:
            done = True
            for index in range(len(self.entries)):
                if not isinstance(self.entries[index], EntryTCP):
                    if type(self.entries[index]) is not str or self.entries[index] == "":
                        # these lines do not pass to EntryTCP constructor
                        self.removed_lines += 1
                        del self.entries[index]
                        done = False
                        break

                    try:
                        self.entries[index] = EntryTCP(self.entries[index])
                    except EntryTCP_Error:
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
