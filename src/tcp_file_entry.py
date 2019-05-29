
from tcp_structs_exceptions import EntryTCP_FormatError
from hexa_manip import ip_from_hexa, port_from_hexa, int_from_string

from src.tcp_structs import C_STATE

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

        issplit = self.string.split(' ')
        ssplit = []

        for item in issplit:
            if item is not '':
                ssplit.append(item)

        if len(self.string) < 120:
            raise EntryTCP_FormatError('Line length not recognized as /proc/net format.', "Length was: {0}".format(len(self.string)))

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
