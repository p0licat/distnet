
from tcp_structs_exceptions import EntryInitError, HexadecimalIpFormatError, \
    HexadecimalPortFormatError, EntryTCP_FormatError, InitializationError
from hexa_manip import ip_from_hexa, port_from_hexa, int_from_string


class C_STATE:
    established     = 0x1
    syn_sent        = 0x2
    syn_recv        = 0x3
    fin_wait1       = 0x4
    fin_wait2       = 0x5
    time_wait       = 0x6
    close           = 0x7
    close_wait      = 0x8
    last_ack        = 0x9
    listen          = 0xA
    tcp_closing     = 0xB

    strings = {
        0x1: "established",
        0x2: "syn_sent",
        0x3: "syn_recv",
        0x4: "fin_wait1",
        0x5: "fin_wait2",
        0x6: "time_wait",
        0x7: "close",
        0x8: "close_wait",
        0x9: "last_ack",
        0xA: "listen",
        0xB: "tcp_closing"
    }

    lower_bound = 0x1
    upper_bound = 0xB

    @staticmethod
    def check_bounds(value):
        """
            Verifies if value inside argument is within class bounds.
            Returns the same value.
            Exceptions:
                ValueError
        """
        sv = C_STATE.lower_bound
        ev = C_STATE.upper_bound
        if value < sv or value > ev:
            raise ValueError("Value provided was out of bounds.")

        return value

    @staticmethod
    def string_from_hex(value):
        C_STATE.check_bounds(value)
        return C_STATE.strings[value] if value in C_STATE.strings else None

    @staticmethod
    def hex_from_string(string):

        if type(string) is not str:
            raise TypeError("Function requires str as argument.")

        if string not in C_STATE.strings.values():
            return None

        for value in range(C_STATE.lower_bound, C_STATE.upper_bound + 1):
            if C_STATE.strings[value] == string:
                return value

        return None


class EntryTCP(object):
    def __init__(self, entry_line):

        if not type(entry_line) is str:
            raise EntryInitError('Entry line must be string. {0}'.format(entry_line), entry_line)


        self.string = entry_line
        if self.string[0] == '\t' or self.string[-1] == '\t':
            self.string = entry_line.strip('\t ')

        self.local_ip = None
        self.dest_ip = None

        self.local_port = None
        self.dest_port = None

        self.state = None


        if len(self.string) < 120:
            raise EntryTCP_FormatError('Line length not recognized as /proc/net format.', "Length was: {0}".format(len(self.string)))

        issplit = self.string.split(' ')
        ssplit = []

        for item in issplit:
            if item is not '':
                ssplit.append(item)

        if len(ssplit) < 2:
            raise EntryTCP_FormatError("Columns were less than expected.", 'Number of columns: {0}, with expected: ??'.format(len(ssplit)))

        if ssplit[0] == 'sl':
            raise EntryTCP_FormatError("Header line.", "Found header line identifier: {0}".format(ssplit[0]))

        entry_number = ssplit[0]
        local_addr_field = ssplit[1]
        dest_addr_field = ssplit[2]
        conn_state = ssplit[3]

        if entry_number[0] == '':
            raise EntryTCP_FormatError('Line is not a valid entry.', "Entry number is null: {0}".format(st[0]))

        s_addr_field = local_addr_field.split(':')
        str_ip = s_addr_field[0]
        str_port = s_addr_field[1]

        ip = ip_from_hexa(str_ip)
        port = port_from_hexa(str_port)

        self.local_ip = ip
        self.local_port = port

        s_addr_field = dest_addr_field.split(':')
        str_ip = s_addr_field[0]
        str_port = s_addr_field[1]

        ip = ip_from_hexa(str_ip)
        port = port_from_hexa(str_port)

        self.dest_ip = ip
        self.dest_port = port

        self.state = conn_state
        # TODO: continue test function untill it's not not done

    def __str__(self):
        rstr = ""
        rstr += "state: " + str(C_STATE.string_from_hex(int_from_string(self.state))) + " "
        rstr += "from: " + str(self.local_ip) + ":" + str(self.local_port) + " "
        rstr += "dest: " + str(self.dest_ip) + ":" + str(self.dest_port) + " "
        rstr += '\n'
        return rstr

class FileTCP(object):
    def __init__(self, path):
        self.path = path
        self.data = None
        self.entries = None
        self.removed_lines = 0

    def parse_entries(self):

        # constructor ?

        if self.data == None:
            raise InitializationError('Fatal error, no data to parse.', 'Tried with path: {0}'.format(self.path))

        self.entries = self.data.split('\n')

        # delete non-entry lines
        while True:
            done = True
            for index in range(len(self.entries)):
                if not isinstance(self.entries[index], EntryTCP):
                    if type(self.entries[index]) is not str or len(self.entries[index]) == 0:
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
                sys.stderr.write('Error, file not accessible.\n')
        else:
            self.data = data

        if self.data == None:
            sys.stderr.write('Nothing was read...')
        else:
            self.parse_entries()

    def print_entries(self):
        for item in self.entries:
            print(str(item))
