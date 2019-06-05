"""
    Entry point.
    TODO: restructure project tree
"""
import argparse

import time

import os
import sys

from tcp_file_handler import FileTCP
from os_check import os_filesystem_check

__version__ = None

#TODO: this is broken.
with open('./VERSION', 'r') as fd:
    __version__ = fd.read()
    fd.close()

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-c", "--continuous", action="store_true", help="refreshes output")
    parser.add_argument("--version", action="store_true", help="prints version of this package")
    #parser.add_argument("-w", "--write") # TODO:

    args = parser.parse_args()
    #print(args)

    if args.version == True:
        print("Version is: " + str(__version__))
        exit(0)

    if args.verbose == True:
        if os_filesystem_check(directory='/proc/net///', files_list=[
            '/tcp',
            '//tcp6',
            'udp',
            'udp6'
        ], filetype_pattern=': empty$'):
            with open('/proc/net/tcp', 'r') as ftcp:
                print(ftcp.read())
                print("End file.\n\n")
            with open('/proc/net/tcp6', 'r') as ftcp:
                print(ftcp.read())
                print("End file.\n\n")

    # 2> /dev/null
    redir_std = open(os.devnull, 'w')
    sys.stderr = redir_std

    time_sleep = 1 # TODO: default-valued int argument argparse

    if args.continuous == True:
        # TODO: catch interrupt signal CTRL+C, OS
        while True:
            ftcp = FileTCP('/proc/net/tcp')
            ftcp.read_tcp_struct()
            ftcp.print_entries()
            time.sleep(1)
            sys.stdout.write("----\n")
    else:
        ftcp = FileTCP('/proc/net/tcp')
        ftcp.read_tcp_struct()
        ftcp.print_entries()

    redir_std.close()
    sys.stdout.write("Done.\n")
    exit(0)

if __name__ == '__main__':
    main()
