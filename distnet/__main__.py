"""
    Entry point.
    TODO: restructure project tree
"""

import socket


import argparse

import time

import os
import sys

from tcp_file_handler import FileTCP
from os_check import os_filesystem_check

import pkg_resources

versionFile = pkg_resources.resource_filename(__name__, 'resources/VERSION')

__version__ = None

with open(versionFile, 'r') as fd:
    __version__ = fd.read()
    fd.close()

def query_ns(ns_ip, dest_ip):
    try:
        return str(socket.gethostbyaddr(dest_ip)[0])
    except socket.herror as he:
        return str("")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-c", "--continuous", action="store_true", help="refreshes output")
    parser.add_argument("--version", action="store_true", help="prints version of this package")
    parser.add_argument("--output", action="append", help="file to write to", type=argparse.FileType('w'))
    parser.add_argument("--ns_list", action="append", help="space separated ip addresses of nameservers to query")

    args = parser.parse_args()

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
    redir_stderr = open(os.devnull, 'w')
    sys.stderr = redir_stderr

    time_sleep = 1 # TODO: default-valued int argument argparse

    if args.output != None:
        fd_args = args.output[0]
        sys.stdout = fd_args

    ns_list = []
    if args.ns_list != None:
        ns_list = args.ns_list

    if args.continuous == True:
        # TODO: catch interrupt signal CTRL+C, OS
        history_ips = dict()
        while True:

            ftcp = FileTCP('/proc/net/tcp')
            ftcp.read_tcp_struct()

            if args.output == None:
                ftcp.print_entries()
                sys.stdout.write("----\n")
            else:
                en = ftcp.get_entries()
                for entry in en:
                    if entry.dest_ip not in history_ips.keys():
                        history_ips[entry.dest_ip] = True
                        ns_formatted = ""
                        for ns_ip in ns_list:
                            sys.stdout.write("Warning: DNS changed to default ... ")
                            ns_formatted += " " + query_ns(ns_ip, entry.dest_ip) + " "
                        sys.stdout.write(entry.dest_ip + ns_formatted + '\n')

            ftcp.draw_map()

            time.sleep(1)
            sys.stdout.flush()
    else:
        ftcp = FileTCP('/proc/net/tcp')
        ftcp.read_tcp_struct()
        ftcp.print_entries()

    redir_std.close()
    sys.stdout.write("Done.\n")

    if args.output != None:
        args.output.close()

    exit(0)

if __name__ == '__main__':
    main()
