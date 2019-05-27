
import sys

class EntryInitError(Exception):
    def __init__(self, message, case):
        super(EntryInitError, self).__init__(message)
        self.string = case
        print(self.string)

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


class EntryTCP(object):
    def __init__(self, entry_line):

        if not type(entry_line) is str:
            raise EntryInitError('Entry line must be string. {0}'.format(entry_line), entry_line)


        self.string = entry_line
        if self.string[0] == '\t' or self.string[-1] == '\t':
            self.string = entry_line.strip('\t ')

        print('el0:::!' + entry_line[1]+'endelim')


        self.local_ip = None
        self.dest_ip = None

        self.local_port = None
        self.dest_port = None

        self.status = None



        # DEBUG
        #for element in self.string.split(' '):
        #    print(element)
        print("st -> " + self.string)
        print("ln -> " + str(len(self.string)))

        if len(self.string) < 120:
            raise EntryTCP_FormatError('Line length not recognized as /proc/net format.', "Length was: {0}".format(len(self.string)))


        # this code sucks TODO DEBUG WHAT
        # st = []
        # print('self.string.split[3]', self.string.split(' ')[3])
        # print('self.string.split[4]', self.string.split(' ')[4])
        #
        # st.append(self.string.split(' ')[3])
        # st.append(self.string.split(' ')[4])
        #
        # print("debug")
        # print(self.string)
        # print(self.string.split(' '))
        # print("len::::")
        # print(len(self.string.split(' ')))
        # print("**debug**")
        # doesn't suck anymore so bad

        print(self.string + '<<<- sstring')
        issplit = self.string.split(' ')
        ssplit = []

        for item in issplit:
            if item is not '':
                ssplit.append(item)

        print(ssplit)

        if len(ssplit) < 2:
            raise EntryTCP_FormatError("Columns were less than expected.", 'Number of columns: {0}, with expected: ??'.format(len(ssplit)))

        entry_number = ssplit[0]
        local_addr_field = ssplit[1]
        dest_addr_field = ssplit[2]

        print(str(entry_number) + '<---enum')

        # should not be st[3] -> st[0]
        if entry_number[0] == '':
            raise EntryTCP_FormatError('Line is not a valid entry.', "Entry number is null: {0}".format(st[0]))

        s_addr_field = local_addr_field.split(':')
        str_ip = s_addr_field[0]
        str_port = s_addr_field[1]

        ip = self.ip_from_hexa(str_ip)
        port = self.port_from_hexa(str_port)

        self.local_ip = ip
        self.local_port = port

        s_addr_field = dest_addr_field.split(':')
        str_ip = s_addr_field[0]
        str_port = s_addr_field[1]

        ip = self.ip_from_hexa(str_ip)
        port = self.port_from_hexa(str_port)

        self.dest_ip = ip
        self.dest_port = port

        # TODO: continue test function untill it's not not done

    def hexa_dict(self):
        # hexa dict generation
        h_dict = {}
        for i in range(0, 10):
            h_dict[str(i)] = i # eww, refactor list comprejenjo
        ind = 10
        for i in 'abcdef':
            h_dict[i] = ind
            h_dict[str(i).upper()] = ind
            ind += 1
        # end hexa dict generation
        return h_dict


    # todo_ rename ip_from_hexa , port_from_hexa
    def ip_from_hexa(self, string):
        h_dict = self.hexa_dict()

        rval = ""
        if len(string) != 8:
            raise HexadecimalIpFormatError('Not a valid IPv4 string.', string)

        s = string[::-1]
        o = []
        while s:
            o.append(s[:2])
            s = s[2:]
        for pair in o:
            value = 0
            i = 0
            for h_char in pair:
                value += pow(16, i) * h_dict[h_char]
                i += 1
            rval += str(value) + '.'
        return rval.rstrip('.')

    def port_from_hexa(self, string):
        # hexa dict generation
        h_dict = self.hexa_dict()

        rval = 0
        if len(string) != 4:
             raise HexadecimalPortFormatError('Not a valid hexadeimal port string.', string)

        s = string[::-1]

        i = 0
        for h_char in s:
            rval += pow(16, i) * h_dict[h_char]
            i += 1
        return str(rval)



class FileTCP(object):
    def __init__(self, path):
        self.path = path
        self.data = None
        self.entries = None

    def parse_entries(self):

        # constructor ?

        if self.data == None:
            raise InitializationError('Fatal error, no data to parse.')

        print("Pre-split:")
        print(self.entries)
        self.entries = self.data.split('\n')
        print("post:")
        print(self.entries)
        print(len(self.entries))

        # delete non-entry lines
        while True:
            done = True
            for index in range(len(self.entries)):
                if not isinstance(self.entries[index], EntryTCP):
                    if type(self.entries[index]) is not str or len(self.entries[index]) == 0:
                        del self.entries[index]
                        done = False
                        break

                    try:
                        self.entries[index] = EntryTCP(self.entries[index])
                        print("test:->>>>" + str(self.entries[index].string))
                    except EntryTCP_FormatError as fe:
                        print("Removing line: ", self.entries[index])
                        del self.entries[index]
                        done = False
                        break
            if done:
                break

        print(self.entries)
        #
        # for index in range(len(self.entries)):
        #     print(len(self.entries[index]))
        #     self.entries[index] = EntryTCP(self.entries[index]) # parser is constructor

        print("Parse done.") # debug

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
            print("parse done e")#deb
