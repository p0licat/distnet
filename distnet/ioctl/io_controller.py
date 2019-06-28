"""
    Module containing file input and output of distnet data.
"""

from tcp_file_entry import EntryTCP
import os


class IO_Ctl:
    def __init__(self, filepath):
        self.__filePath = None

        if os.path.exists(filepath):
            self.__filePath = filepath
        else:
            raise FileExistsError("")


    def print_data(self):
        with open(self.__filePath, 'r') as fd:
            print(fd.read().split('\n'))

    @staticmethod
    def check_entries_list(entries):
        try:
            if not isinstance(entries, list):
                raise TypeError("")
            for item in entries:
                if not isinstance(item, EntryTCP):
                    raise TypeError()
        except TypeError:
            return False
        return True

    @staticmethod
    def write_to_screen(entries, mode=None):
        if not IO_Ctl.check_entries_list(entries):
            return

        for entry in entries:
            f_str = ""
            f_str += entry.dest_ip

            if mode == 'host' or mode == 'location':
                f_str += ','
                f_str += entry.resolved_hostname
                f_str += ','
            if mode == 'location':
                f_str += entry.resolved_location
            f_str += '\n'

            print(f_str)

    def write_to_file(self, entries):
        if not IO_Ctl.check_entries_list(entries):
            return

        try:
            with open(self.__filePath, 'w') as fd:
                for entry in entries:
                    f_str = ""
                    f_str += entry.dest_ip
                    f_str += ','
                    f_str += entry.resolved_hostname
                    f_str += ','
                    f_str += entry.resolved_location
                    f_str += '\n'
                    fd.write(f_str)

                fd.close()
        except Exception as ex:
            print(ex) # NoneType check!X
            fd.close() #>?

    def read_from_file(self):
        r_entries = list()
        with open(self.__filePath, 'r') as fd:
            data = fd.read().split('\n')
            for line in data:
                line = line.split(',')
                if len(line) < 3:
                    continue
                dest_ip = line[0]
                r_hostname = line[1]
                r_location = line[2]

                try:
                    etcp = EntryTCP("0: 00000000:0000 00000000:0000 01 00000000:00000000 00:00000000 00000000  1000        0 29965 1 ffff932537491800 24 4 30 10 -1")
                    etcp.dest_ip = dest_ip
                    etcp.resolved_hostname = r_hostname
                    etcp.resolved_location = r_location
                    r_entries.append(etcp)
                except Exception as ex:
                    print(ex)
                    continue

        return r_entries
