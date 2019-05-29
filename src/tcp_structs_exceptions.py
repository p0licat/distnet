
import sys

#TODO: restructure exceptions and inheritance
class InitializationError(Exception):
    def __init__(self, message, case):
        super(InitializationError, self).__init__(message)
        self.string = case
        sys.stderr.write(self.string)

class EntryInitError(Exception):
    def __init__(self, message, case):
        super(EntryInitError, self).__init__(message)
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

class EntryTCP_FormatError(Exception):
    def __init__(self, message, case):
        super(EntryTCP_FormatError, self).__init__(message)
        sys.stderr.write(case)
