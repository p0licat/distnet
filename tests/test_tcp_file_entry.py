"""
    Tests for EntryTCP class.
    TODO: import from FileTCP tests?
"""

import re
import pytest

from src.tcp_structs import C_STATE
from src.tcp_file_entry import EntryTCP
from src.hex_manip import int_from_string

@pytest.fixture
def EntryTCP_testing():
    data = "0: F100A8C0:CDF4 E511D9AC:01BB 01 00000000:00000000 00:00000000 00000000  1000        0 29965 1 ffff932537491800 24 4 30 10 -1"
    etcp = EntryTCP(data)
    return etcp

def check_field_ip(field):
    re_ipaddr_mchr = re.compile(r'[\.0-9]')
    assert type(field) is str
    assert len(field) > 7 and len(field) < 17
    for char in field:
        assert type(char) is str
        assert len(char) == 1
        assert re_ipaddr_mchr.match(char) != None

def check_field_port(field):
    re_port_mchr = re.compile(r'[0-9]')
    assert type(field) is str
    assert len(field) > 0 and len(field) <= 5
    for char in field:
        assert type(char) is str and len(char) == 1
        assert re_port_mchr.match(char) != None
    # try conversion to int
    try:
        port = int(field)
        assert True
        assert port >= 0 and port <= 65535
    except Exception as ex:
        assert False

def check_field_state(field):
    # TODO: add regex
    re_connection_state_mchr = re.compile(r'[0-9A-F]{1,2}') # TODO: not used

    assert type(field) is not None
    assert type(field) is str

    # regex check
    for char in field:
        assert re_connection_state_mchr.match(char)

    # try conversion to int
    try:
        int_from_string(field)
    except Exception as ex:
        assert False

    assert type(int_from_string(field)) is int
    state_int = int_from_string(field)

    # conversion test
    assert type(C_STATE.string_from_hex(state_int)) is str
    assert C_STATE.hex_from_string( C_STATE.string_from_hex(state_int) ) == state_int


def check_field_string(string):
    assert type(string) is str
    assert len(string) > 100 # TODO: cross check


def test_EntryTCP_instance(EntryTCP_testing):
    try:
        etcp = EntryTCP_testing
    except Exception as ex:
        print(ex)
        assert False

    assert isinstance(etcp, EntryTCP)
    check_field_ip(etcp.local_ip)
    check_field_ip(etcp.dest_ip)
    check_field_port(etcp.local_port)
    check_field_port(etcp.dest_port)
    check_field_state(etcp.state)
