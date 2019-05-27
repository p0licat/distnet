
from src.main import os_filesystem_check
from src.tcp_structs import FileTCP, EntryTCP

import re

def test_os_filesystem_check():
    try:
        os_filesystem_check()
        assert False
    except TypeError as te:
        assert True

    assert os_filesystem_check(directory='/proc/net///', files_list=[
        '/tcp',
        '//tcp6',
        'udp',
        'udp6'
    ], filetype_pattern=': empty$') == True

    assert os_filesystem_check(directory='/proc/exists/', files_list=[
        'tcp',
        'udp'
    ], filetype_pattern=': empty$') == False

    assert os_filesystem_check(directory='/proc/net', files_list=[
        'tcp12',
        'udp12'
    ], filetype_pattern=': empty$') == False

def test_read_tcp_struct():

    tcp_path = '/proc/net/tcp'

    tcpf = FileTCP(tcp_path)
    #tcpf.read_tcp_struct() DEBUG WHAT

    #assert tcpf.data != None

    assert type(tcpf) is FileTCP
    #assert type(tcpf.data) is str
    #assert type(tcpf.entries) is list

    from_file = True

    #if len(tcpf.entries) == 0:
    if tcpf.entries is None:
        tcp_file_data = "0: F100A8C0:CDF4 E511D9AC:01BB 01 00000000:00000000 00:00000000 00000000  1000        0 29965 1 ffff932537491800 24 4 30 10 -1 \n\
            1: F100A8C0:A126 0E15D9AC:01BB 01 00000000:00000000 00:00000000 00000000  1000        0 50310 1 ffff93258a38f000 24 4 30 10 -1 \n\
            2: F100A8C0:8510 26FB1934:01BB 01 00000000:00000000 02:0000A574 00000000  1000        0 30924 2 ffff9325b2832000 46 4 25 10 -1 \n\
        "

        tcpf.read_tcp_struct(tcp_file_data)

        assert type(tcpf.entries) is list
        assert tcpf.entries != []

        print("done tcps")
        from_file = not from_file


    if len(tcpf.entries) > 0 or not from_file:

        #regular patterns for /proc/net/tcp file
        re_ipaddr_mchr = re.compile(r'[\.0-9]')
        re_port_mchr = re.compile(r'[0-9]')
        #re_connection_state_mchr
        #re_hexadecimal_str_mchr_line r'[0-9abcdefABCDEF\.]{7, 17}'
        #re_hexa_addr_mchr_line r'[0-9abcdefABCDEF]{1,5}'
        assert len(tcpf.entries) > 0
        for entry in tcpf.entries:
            #assert False
            assert isinstance(entry, EntryTCP)
            #assert False
            assert type(entry.string) is str

            assert type(entry.local_ip) is str
            assert len(entry.local_ip) > 7 and len(entry.local_ip) < 17
            for char in entry.local_ip:
                assert type(char) is str
                assert len(char) == 1
                assert re_ipaddr_mchr.match(char) != None

            assert type(entry.local_port) is str
            assert len(entry.local_port) > 0 and len(entry.local_port) <= 5
            for char in entry.local_port:
                assert type(char) is str and len(char) == 1
                assert re_port_mchr.match(char) != None

            try:
                port = int(entry.local_port)
                assert True
                assert port >= 0 and port <= 65535
            except Exception as ex:
                assert False

            assert type(entry.dest_ip) is str
            assert entry.dest_ip != None
            assert len(entry.dest_ip) > 7 and len(entry.dest_ip) < 17
            for char in entry.dest_ip:
                assert type(char) is str and len(char) == 1
                assert re_ipaddr_mchr.match(char) != None


            assert type(entry.dest_port) is str
            assert len(entry.dest_port) > 0 and len(entry.dest_port) < 5
            for char in entry.dest_port:
                assert type(char) is str and len(char) == 1
                assert re_port_mchr.match(char) != None

            try:
                port = int(entry.dest_port)
                assert True
                assert port >= 0 and port <= 65535
            except Exception as ex:
                assert False

        # TODO: continue test function untill it's not not done
        # test for existing file
