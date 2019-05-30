import re
import sys
import pytest


from src.tcp_structs import C_STATE
from src.tcp_structs_exceptions import EntryTCP_FormatError
from src.tcp_file_handler import FileTCP, EntryTCP
from src.hex_manip import int_from_string

from test_tcp_file_entry import     check_field_ip, \
                                    check_field_string, \
                                    check_field_port, \
                                    check_field_state

#regular patterns for /proc/net/tcp file
re_ipaddr_mchr = re.compile(r'[\.0-9]')
re_port_mchr = re.compile(r'[0-9]')

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

    # entries populated
    assert type(tcpf.entries) is list
    assert tcpf.entries != [] # tests fail without networking enabled!
    assert len(tcpf.entries) > 0

    # check entry list
    for entry in tcpf.entries:
        assert isinstance(entry, EntryTCP)

        try:
            check_field_string(entry.string)
        except:
            assert False

        try:
            check_field_ip(entry.local_ip)
            check_field_ip(entry.dest_ip)
        except:
            assert False

        try:
            check_field_port(entry.local_port)
            check_field_port(entry.dest_port)
        except:
            assert False

        try:
            check_field_state(entry.state)
        except:
            assert False

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

        try:
            check_field_string(entry.string)
        except:
            assert False

        try:
            check_field_ip(entry.local_ip)
            check_field_ip(entry.dest_ip)
        except:
            assert False

        try:
            check_field_port(entry.local_port)
            check_field_port(entry.dest_port)
        except:
            assert False

        try:
            check_field_state(entry.state)
        except:
            assert False

    # TODO: continue test function untill it's not not done


def test_print_entries():

    tcp_path = "/proc/net/tcp"
    tcpf = FileTCP(tcp_path)
    tcpf.read_tcp_struct()

    # todo: simulate stdout # TODO: stream tests
    try:
        tcpf.print_entries()
    except Exception as ex:
        sys.stderr.write(str(ex))
        assert False

    assert type(tcpf.entries) is list
    for i in tcpf.entries:
        assert isinstance(i, EntryTCP)
