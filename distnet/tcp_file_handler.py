"""
    File parser and syntax analysis class, for /proc/net/tcp.
"""

import re
import os
import sys

import time
import tempfile

import pygal

from network_controller import resolve_hostname, resolve_location
from game_controller import GameController
from tcp_file_entry import EntryTCP
from tcp_structs_exceptions import  EntryTCP_Error, \
                                    EntryTCP_FormatError, \
                                    FileTCP_InitError


import socket # TODO: bad exception handling with socket.gaierror

class FileTCP(object):
    """
        File data parser.
    """
    def __init__(self, path):
        self.re_path_mchr = re.compile(r'[a-zA-Z0-9\_\/]') # TODO: practice?
        self.path = path
        self.data = None
        self.entries = None
        self.removed_lines = 0

        self.entry_locations = dict()
        self.entry_hostnames = dict()
        self.tempfile_name = None
        self.tempfile_handler = None
        self.last_write_filename = None

        self.game_controller = None
        self.running = True

        if not isinstance(path, str) or path == "":
            raise FileTCP_InitError("Not a valid path string: ", "{0}".format(path))

        for s_chr in path:
            if not self.re_path_mchr.match(s_chr):
                raise FileTCP_InitError('Path contains invalid characters.', s_chr) # TODO: exception style

    def __del__(self):
        if self.tempfile_name is not None:
            os.remove(self.tempfile_name)

    def parse_entries(self):
        """
            If self.data is populated with the /net/tcp text file's read data,
            it is analyzed by parse_entries for syntax checking, and passing
            lines will be converted into EntryTCP objects and stored in object
            self.entries.
        """
        # TODO: InitError as superclass of FileTCP_NoDataError, msg len
        # TODO: exception for empty file? tests for empty file? test for connectivity?
        if self.data is None:
            raise FileTCP_InitError("Fatal error, no data to parse.", "Tried with path: {0}".format(self.path))

        self.old_entries = self.entries
        self.entries = self.data.split("\n")

        # delete non-entry lines
        while True:
            done = True
            for index in range(len(self.entries)):
                if not isinstance(self.entries[index], EntryTCP):
                    if not isinstance(self.entries[index], str) or self.entries[index] == "":
                        # these lines do not pass to EntryTCP constructor
                        self.removed_lines += 1
                        del self.entries[index]
                        done = False
                        break


                    try:
                        self.entries[index] = EntryTCP(self.entries[index])

                        if self.old_entries != None:
                            found = False
                            for item_new in self.old_entries:
                                if str(self.entries[index]) == str(item_new):
                                    found = True
                            if found:
                                del self.entries[index]
                                done = False
                                break
                    except EntryTCP_FormatError:
                        # lines with incorrect format are removed
                        self.removed_lines += 1
                        del self.entries[index]
                        done = False
                        break


            if done:
                break

        if self.old_entries != None:
            for item in self.old_entries:
                found = False
                for item_new in self.entries:
                    if str(item) == str(item_new):
                        found = True

                if not found:
                    self.entries.append(item)
                else:
                    print("EXCEPT")

    def read_tcp_struct(self, data=None):
        """
            Initializes self.data property with either function argument or from
            file data pointed to by self.path.
        """
        if data is None:
            try:
                with open(self.path, 'r') as tcp_fd:
                    self.data = tcp_fd.read()
            except IOError as io_e:
                # Errno 2 not exist
                sys.stderr.write(str(io_e))
                sys.stderr.write("Error, file not accessible.\n")
        else:
            self.data = data

        if self.data is None:
            sys.stderr.write("Nothing was read...")
        else:
            self.parse_entries()

    def get_entries(self):
        """
            Getter for public field.
        """
        return self.entries


    def draw_map_v3(self, mode = None, continuous = None, visual = None):

        worldmap_chart = pygal.maps.world.World()
        worldmap_chart.title = 'Some countries'


        if self.tempfile_name == None:
            new_file, filename = tempfile.mkstemp(suffix='.png')
            self.tempfile_name = str(filename)
            self.last_write_name = self.tempfile_name

            os.close(new_file)
            worldmap_chart.render_to_png(self.tempfile_name)
            #wordlmap_chart.render_to_png(self.loading_png_file)
            # if not continuous:
            #     self.tempfile_name = None
        #else:
        #    worldmap_chart.render_to_png(self.tempfile_name)


        if visual == True:
            if self.game_controller == None:
                self.game_controller = GameController(self.tempfile_name)

            self.running = self.game_controller.world()

        for entry in self.entries:
            if visual == True:
                self.running = self.game_controller.world()
            if not self.running and continuous:
                break
            if entry.resolved_location != None:
                self.entry_locations[entry.dest_ip] = entry.resolved_location
            else:
                if entry.resolved_location == None:
                    entry.resolve_country()
                if entry.resolved_location != None:
                    self.entry_locations[entry.dest_ip] = entry.resolved_location


        if mode == None or mode == 'flag':
            for item in self.entry_locations.keys():
                val = self.entry_locations[item]
                worldmap_chart.add(item, val)
                print('test')
                print('added: ' + str(item) + ' ... ' + str(val))
        elif mode == 'heatmap':
            worldmap_chart.add('Heatmap', self.entry_locations.values())

        time.sleep(1)
        worldmap_chart.render_to_png(self.tempfile_name)
        time.sleep(1)


        if not continuous:
            self.tempfile_name = None
        if visual == True:
            self.running = self.game_controller.world()


    def print_entries(self, resolve=False):
        """
            Prints EntryTCP objects to stdout, one item per line.
        """
        for item in self.entries:
            if not resolve:
                sys.stdout.write(str(item))
            else:
                resolved_host = ""
                try:
                    resolved_host = resolve_hostname(str(item.dest_ip))
                except socket.gaierror as ge:
                    resolved_host = "UNKNOWN_HOSTNAME"
                sys.stdout.write(str(item).rstrip() + " \t" + str(resolved_host) + " "  + " " + '\n')

    def attempt_resolves(self):
        for entry in self.entries:
            # print("rl: ")
            # print(entry.resolved_location)
            if entry.resolved_location == None:
                entry.resolve_country()
            # print(entry.resolved_location)
            # print("/rl")
