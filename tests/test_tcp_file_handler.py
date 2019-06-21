import os
import re
import sys
import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../distnet"))

# import distnet
from tcp_structs import C_STATE
from tcp_structs_exceptions import EntryTCP_FormatError
from tcp_file_handler import FileTCP
from tcp_file_entry import EntryTCP
from hex_manip import int_from_string

from tests.test_tcp_file_entry import   check_field_ip, \
                                        check_field_string, \
                                        check_field_port, \
                                        check_field_state

from distnet.tcp_structs_exceptions import FileTCP_Error, FileTCP_InitError
#regular patterns for /proc/net/tcp file
re_ipaddr_mchr = re.compile(r'[\.0-9]')
re_port_mchr = re.compile(r'[0-9]')

re_hexadecimal_str_mchr_line = re.compile(r'[0-9abcdefABCDEF\.]{7,17}') # TODO: use in hexadecimal data getter
re_hexa_addr_mchr_line = re.compile(r'[0-9abcdefABCDEF]{1,5}') # TODO: use in hexadecimal data getter


tcp_path = 'tests/chroot/proc/net/tcp'
not_accessible_path = 'tests/chroot/proc/net/notaccessible'

if "TRAVIS" in os.environ and os.environ["TRAVIS"] == "str_true":
    tcp_path = 'tests/chroot/proc/net/tcp'

@pytest.fixture
def FileTCP_testing():
    return FileTCP(tcp_path)

@pytest.fixture
def FileTCP_testing_PathNotAccessible():
    return FileTCP(not_accessible_path)

def test_tcp_file_handler_InitFails():
    with pytest.raises(Exception) as exception_info:
        FileTCP(13)
    assert exception_info.typename == "FileTCP_InitError"

    with pytest.raises(Exception) as exception_info:
        FileTCP("\'proc\'")
    assert exception_info.typename == "FileTCP_InitError"

    with pytest.raises(Exception) as exception_info:
        FileTCP("]]proc]")
    assert exception_info.typename == "FileTCP_InitError"

def test_read_tcp_struct_file(FileTCP_testing):

    tcpf = FileTCP_testing

    # test initial values
    assert type(tcpf) is FileTCP
    assert type(tcpf.path) is str and tcpf.path == tcp_path
    assert type(tcpf.data) is type(None)
    assert type(tcpf.entries) is type(None)


    with pytest.raises(Exception) as exception_info:
        tcpf.parse_entries()
    assert exception_info.typename == "FileTCP_InitError"


    tcpf.read_tcp_struct() # read from file

    # entries populated
    assert type(tcpf.entries) is list
    assert tcpf.entries != [] # tests fail without networking enabled or empty file
    assert len(tcpf.entries) > 0

    # check entry list
    for entry in tcpf.entries:
        print(type(entry))

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


def test_read_tcp_struct_PathNotAccessible(FileTCP_testing_PathNotAccessible):
    if "TRAVIS" in os.environ and os.environ["TRAVIS"] == "str_true":
        pass
    else:
        pytest.skip("TravisCI does not support.")

    tcpf = FileTCP_testing_PathNotAccessible
    tcpf.read_tcp_struct()

    assert tcpf.data == None


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


def test_print_entries_resolve():

    tcp_path = "/proc/net/tcp"
    tcpf = FileTCP(tcp_path)
    tcpf.read_tcp_struct()

    # todo: simulate stdout # TODO: stream tests
    try:
        tcpf.print_entries(resolve=True)
    except Exception as ex:
        sys.stderr.write(str(ex))
        assert False

    assert type(tcpf.entries) is list
    for i in tcpf.entries:
        assert isinstance(i, EntryTCP)

def test_get_entries(FileTCP_testing):
    tcpf = FileTCP_testing
    tcpf.read_tcp_struct()
    tcpf.get_entries()


# def test_draw_map_v2(FileTCP_testing):
#
#     tcpf = FileTCP_testing
#     tcpf.read_tcp_struct()
#     tcpf.draw_map_v2()
#     #assert tcpf.tempfile_name != None
#     #assert os.path.isfile(tcpf.tempfile_name)
#
#     # second render_to_png
#     tcpf.draw_map_v2()
#
#
# def test_draw_map_v2_heatmap(FileTCP_testing):
#
#     tcpf = FileTCP_testing
#     tcpf.read_tcp_struct()
#     tcpf.draw_map_v2(mode='heatmap')
#     #assert tcpf.tempfile_name != None
#     #assert os.path.isfile(tcpf.tempfile_name)
#
#     # second render_to_png
#     tcpf.draw_map_v2(mode='heatmap')


def test_draw_map_v3(FileTCP_testing):

    tcpf = FileTCP_testing
    tcpf.read_tcp_struct()
    tcpf.draw_map_v3()
    #assert os.path.isfile(tcpf.tempfile_name)

    # second render_to_png
    tcpf.draw_map_v3()
    #assert tcpf.tempfile_name != None
    #TODO: if draw twice, then delete
    # if draw once, keep ... ?


def test_draw_map_v3_heatmap(FileTCP_testing):

    tcpf = FileTCP_testing
    tcpf.read_tcp_struct()
    tcpf.draw_map_v3(mode='heatmap')
    #assert tcpf.tempfile_name != None
    #assert os.path.isfile(tcpf.tempfile_name)

    # second render_to_png
    tcpf.draw_map_v3(mode='heatmap')
