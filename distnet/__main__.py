"""
    Entry point.
"""

import signal
import argparse
import time
import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../distnet"))

from ioctl.io_controller import IO_Ctl
from networking.network_controller import resolve_hostname
from tcp.tcp_file_handler import FileTCP
from utils.os_check import os_filesystem_check


import pkg_resources

versionFile = pkg_resources.resource_filename(__name__, 'resources/VERSION')

__version__ = None

with open(versionFile, 'r') as fd:
    __version__ = fd.read()
    fd.close()


def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)


def main():

    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true", help="test os filesystem")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-c", "--continuous", action="store_true", help="continuously update output")
    parser.add_argument("-r", "--resolve", action="store_true", help="resolve ip addresses to hostnames")
    parser.add_argument("-o", "--output", action="append", help="file to write to", type=argparse.FileType('w'))
    parser.add_argument("--visual", action="store_true", help="draw on world map (use with -c)")
    parser.add_argument("--version", action="store_true", help="prints version of this package")
    parser.add_argument("--mode", action="append", help="heatmap or flag")


    args = parser.parse_args()

    if args.mode != None:
        args.mode = args.mode[0]

    if args.version == True:
        print("Version is: " + str(__version__))
        exit(0)

    if args.test == True:
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
        exit(0)

    # 2> /dev/null
    # redir_stderr = open(os.devnull, 'w')
    # sys.stderr = redir_stderr

    time_sleep = 1 # TODO: default-valued int argument argparse

    if args.continuous == True:
        history_ips = dict()
        cdict = dict()

        ftcp = FileTCP('/proc/net/tcp')
        while ftcp.running:

            ftcp.read_tcp_struct()

            if args.verbose == True:
                print(ftcp.data)

            if args.output == None:

                if args.resolve == True:
                    if args.verbose == True:
                        print("Resolving addresses...")
                    ftcp.attempt_resolves()
                en = ftcp.get_entries()
                if ftcp.read_changed:
                    IO_Ctl.write_to_screen(en, mode='location' if args.resolve == True else None)

                time.sleep(1)
            else:
                if args.verbose == True:
                    print("Attempting resolves...")
                ftcp.attempt_resolves()
                if args.verbose:
                    print("Resolved.")
                en = ftcp.get_entries()
                args.output[0].close()
                ic = IO_Ctl(args.output[0].name)
                #print("Writing to file...")
                ic.write_to_file(en)
                time.sleep(1)

            if args.visual == True:
                ftcp.draw_map_v3(mode = args.mode, continuous = args.continuous, visual=True)

            sys.stdout.flush()
    else:
        if args.output != None:
            fd_args = args.output[0]
            sys.stdout = fd_args

        ftcp = FileTCP('/proc/net/tcp')
        ftcp.read_tcp_struct()

        if args.verbose == True:
            print(ftcp.data)

        ftcp.print_entries(resolve=args.resolve)

        if args.visual == True:
            ftcp.draw_map_v3(mode = args.mode, continuous = args.continuous)
            print("Wrote image to: " + ftcp.last_write_name)


    #redir_std.close()
    sys.stdout.write("Done.\n")

    if args.output != None:
        args.output[0].close()

    exit(0)

if __name__ == '__main__':
    main()
