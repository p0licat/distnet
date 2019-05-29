
from tcp_structs import FileTCP
from os_check import os_filesystem_check

def main():
    if os_filesystem_check(directory='/proc/net///', files_list=[
        '/tcp',
        '//tcp6',
        'udp',
        'udp6'
    ], filetype_pattern=': empty$'):
        with open('/proc/net/tcp', 'r') as ftcp:
            print(ftcp.read())
        with open('/proc/net/tcp6', 'r') as ftcp:
            print(ftcp.read())

    ftcp = FileTCP('/proc/net/tcp')
    ftcp.read_tcp_struct()
    ftcp.print_entries()

    sys.stdout.write("Done.\n")
    exit(0)

if __name__ == '__main__':
    main()
