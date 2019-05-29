import re

import sys

import pytest


from src.tcp_structs import C_STATE
from src.tcp_structs_exceptions import EntryTCP_FormatError

from src.tcp_file_handler import FileTCP, EntryTCP

from src.hexa_manip import int_from_string

#regular patterns for /proc/net/tcp file
re_ipaddr_mchr = re.compile(r'[\.0-9]')
re_port_mchr = re.compile(r'[0-9]')
re_connection_state_mchr = re.compile(r'[0-9]{1,2}') # TODO: not used
re_hexadecimal_str_mchr_line = re.compile(r'[0-9abcdefABCDEF\.]{7,17}') # TODO: use in hexadecimal data getter
re_hexa_addr_mchr_line = re.compile(r'[0-9abcdefABCDEF]{1,5}') # TODO: use in hexadecimal data getter


tcp_path = '/proc/net/tcp'

@pytest.fixture
def FileTCP_testing():
    return FileTCP(tcp_path)

def test_read_tcp_struct_file(FileTCP_testing):

    tcpf = FileTCP_testing

    # test initial values
    assert type(tcpf) is FileTCP
    assert type(tcpf.path) is str and tcpf.path == tcp_path
    assert type(tcpf.data) is type(None)
    assert type(tcpf.entries) is type(None)

    tcpf.read_tcp_struct() # read from file

    assert type(tcpf.entries) is list
    assert tcpf.entries != []

    assert len(tcpf.entries) > 0

    assert len(tcpf.entries) > 0
    for entry in tcpf.entries:

        assert isinstance(entry, EntryTCP)
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

        assert type(entry.state) is not None
        assert type(entry.state) is str

        # TODO: entry.state int?
        try:
            int_from_string(entry.state)
        except Exception as ex:
            sys.stderr.write(ex)
            assert False

        assert type(int_from_string(entry.state)) is int
        state_int = int_from_string(entry.state)

        assert type(C_STATE.string_from_hex(state_int)) is str
        assert C_STATE.hex_from_string( C_STATE.string_from_hex(state_int) ) == state_int


def test_read_tcp_struct_string(FileTCP_testing):

    tcpf = FileTCP_testing

    # test initial values
    assert type(tcpf) is FileTCP
    assert type(tcpf.path) is str and tcpf.path == tcp_path
    assert type(tcpf.data) is type(None)
    assert type(tcpf.entries) is type(None)

    tcp_file_data = "0: F100A8C0:CDF4 E511D9AC:01BB 01 00000000:00000000 00:00000000 00000000  1000        0 29965 1 ffff932537491800 24 4 30 10 -1 \n\
        1: F100A8C0:A126 0E15D9AC:01BB 01 00000000:00000000 00:00000000 00000000  1000        0 50310 1 ffff93258a38f000 24 4 30 10 -1 \n\
        2: F100A8C0:8510 26FB1934:01BB 01 00000000:00000000 02:0000A574 00000000  1000        0 30924 2 ffff9325b2832000 46 4 25 10 -1 \n\
    "

    tcpf.read_tcp_struct(tcp_file_data) # read from data string

    assert type(tcpf.entries) is list
    assert tcpf.entries != []

    assert len(tcpf.entries) > 0

    assert len(tcpf.entries) > 0
    for entry in tcpf.entries:

        assert isinstance(entry, EntryTCP)
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

        assert type(entry.state) is not None
        assert type(entry.state) is str

        # TODO: entry.state int?
        try:
            int_from_string(entry.state)
        except:
            assert False

        assert type(int_from_string(entry.state)) is int
        state_int = int_from_string(entry.state)

        assert type(C_STATE.string_from_hex(state_int)) is str
        assert C_STATE.hex_from_string( C_STATE.string_from_hex(state_int) ) == state_int


    # TODO: continue test function untill it's not not done
    # test for existing file


def test_print_entries():
    tcp_path = "/proc/net/tcp"
    tcpf = FileTCP(tcp_path)
    tcpf.read_tcp_struct()

    # todo: simulate stdout
    try:
        tcpf.print_entries()
    except Exception as ex:
        sys.stderr.write(str(ex))
        assert False

    assert type(tcpf.entries) is list
    for i in tcpf.entries:
        assert isinstance(i, EntryTCP)
