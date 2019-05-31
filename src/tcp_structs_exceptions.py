
import sys


#TODO: restructure exceptions and inheritance

class EntryTCP_Error(Exception):
    def __init__(self, message):
        super(EntryTCP_Error, self).__init__(message)

class EntryTCP_FormatError(EntryTCP_Error):
    def __init__(self, message, case):
        super(EntryTCP_FormatError, self).__init__(message)
        sys.stderr.write(case)

class EntryTCP_InitError(EntryTCP_Error):
    def __init__(self, message, case):
        super(EntryTCP_InitError, self).__init__(message)
        self.string = str(case)
        sys.stderr.write(self.string)

class HexadecimalStringFormatError(Exception):
    def __init__(self, message, case):
        super(HexadecimalStringFormatError, self).__init__(message)
        self.string = case
        sys.stderr.write(self.string)

class HexadecimalIpFormatError(Exception):
    def __init__(self, message, case):
        super(HexadecimalIpFormatError, self).__init__(message)
        self.string = case
        sys.stderr.write(self.string)

class HexadecimalPortFormatError(Exception):
    def __init__(self, message, case):
        super(HexadecimalPortFormatError, self).__init__(message)
        self.string = case
        sys.stderr.write(self.string)

class FileTCP_Error(Exception):
    def __init__(self, message):
        super(FileTCP_Error, self).__init__(message)

class FileTCP_InitError(FileTCP_Error):
    def __init__(self, message, case):
        super(FileTCP_InitError, self).__init__(message)
        self.string = case
        sys.stderr.write(self.string)
