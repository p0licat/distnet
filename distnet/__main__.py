"""
    Entry point.
    TODO: restructure project tree
"""

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import signal


import argparse

import time

import os
import sys

from network_controller import resolve_hostname
from tcp_file_handler import FileTCP
from os_check import os_filesystem_check


import pkg_resources

versionFile = pkg_resources.resource_filename(__name__, 'resources/VERSION')

__version__ = None

with open(versionFile, 'r') as fd:
    __version__ = fd.read()
    fd.close()


def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        running = False
        sys.exit(0)


#TODO: refactor into game controller class
def world(x, y, gameDisplay_obj, img_location):
    try:
        gameDisplay_obj.blit(pygame.image.load(img_location), (x, y))
    except pygame.error as pe:
        print('frame rdop')







def main():

    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", action="store_true", help="test os filesystem")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("--visual", action="store_true", help="draw on world map (use with -c)")
    parser.add_argument("-c", "--continuous", action="store_true", help="continuously update output")
    parser.add_argument("--version", action="store_true", help="prints version of this package")
    parser.add_argument("--output", action="append", help="file to write to", type=argparse.FileType('w'))
    parser.add_argument("-r", "--resolve", action="store_true", help="resolve ip addresses to hostnames")


    args = parser.parse_args()

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

    if args.output != None:
        fd_args = args.output[0]
        sys.stdout = fd_args

    if args.continuous == True:
        history_ips = dict()
        cdict = dict()

        gameDisplay = None
        if args.visual == True:
            pygame.init()
            pygame.mixer.quit()
            gameDisplay = pygame.display.set_mode((800, 600))
            pygame.display.set_caption('Visualizer')

        if args.visual == True:
            clock = pygame.time.Clock()

        ftcp = FileTCP('/proc/net/tcp')
        running = True
        while running:

            ftcp.read_tcp_struct()

            if args.verbose == True:
                print(ftcp.data)

            if args.output == None:

                en = ftcp.get_entries()

                for entry in en:
                    if entry.dest_ip not in history_ips.keys():
                        history_ips[entry.dest_ip] = True
                        ns_formatted = ""

                        # if args.visual == True:
                        #     tdata = query_whois(query_ns(entry.dest_ip))
                        #     try:
                        #         tdata = tdata.text
                        #     except AttributeError as ae:
                        #         continue
                        #     #print("rvalue text: ")
                        #     #print(tdata)
                        #     cdata = []
                        #     for i in tdata.split('\n'):
                        #         if 'Registrant Country:' in i:
                        #             ccode = i.split(' ')[2].rstrip('\r').rstrip('\n').rstrip()
                        #             ccode = ccode.lower()
                        #             cdata.append(ccode)
                        #             cdict[ccode] = 1 if ccode not in cdict else cdict[ccode] + 1
                        #
                        #     for i in cdata:
                        #         print(cdata)

                        if args.resolve == True:
                            ns_formatted += " " + resolve_hostname(entry.dest_ip) + " "  + " "

                        sys.stdout.write(entry.dest_ip + ns_formatted + '\n')
            else:
                en = ftcp.get_entries()
                for entry in en:
                    if entry.dest_ip not in history_ips.keys():
                        history_ips[entry.dest_ip] = True
                        ns_formatted = ""
                        # !!!!!!
                        sys.stdout.write("Warning: DNS changed to default ... ")
                        ns_formatted += " " + query_ns(ns_ip, entry.dest_ip) + " " + query_whois(query_ns(ns_ip, entry.dest_ip)).__dict__ + " EOFF "
                        sys.stdout.write(entry.dest_ip + ns_formatted + '\n')

            if args.visual == True:
                ftcp.draw_map_v2()

                world(0, 0, gameDisplay, ftcp.tempfile_name)
                pygame.display.update()
                clock.tick(24)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False


            #time.sleep(1)
            sys.stdout.flush()
    else:
        ftcp = FileTCP('/proc/net/tcp')
        ftcp.read_tcp_struct()

        if args.verbose == True:
            print(ftcp.data)

        ftcp.print_entries(resolve=args.resolve)

        if args.visual == True:
            ftcp.draw_map_v2(mode='heatmap')
            print("Wrote image to: " + ftcp.tempfile_name)


    #redir_std.close()
    sys.stdout.write("Done.\n")

    if args.output != None:
        args.output.close()

    exit(0)

if __name__ == '__main__':
    main()