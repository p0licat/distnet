
import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../distnet"))

from tcp_file_handler import FileTCP
from tcp_file_entry import EntryTCP
from ioctl import io_controller
import pytest

@pytest.fixture
def FileTCP_testing():
    return FileTCP('tests/chroot/proc/net/tcp')

@pytest.fixture
def IO_Ctl_fixture():
    try:
        return io_controller.IO_Ctl('tests/chroot/home/testinput')
    except Exception as ex:
        assert False


def check_delete_file():
    with open('tests/chroot/home/testinput', 'w') as fd:
        fd.write()
        fd.close()

def test_init():
    try:
        ioctl_m = io_controller.IO_Ctl("notapath")
        assert False
    except FileExistsError:
        pass

def test_init_success(IO_Ctl_fixture):
    try:
        ioctl_m = IO_Ctl_fixture
    except Exception as ex:
        assert False

def test_IO_write(FileTCP_testing, IO_Ctl_fixture):
    ftcp = FileTCP_testing
    ftcp.read_tcp_struct()
    elist = ftcp.get_entries()
    for entry in elist:
        entry.resolve_country() # waiting for pull
    try:
        IO_Ctl_fixture.write_to_file(elist)
    except Exception as ex:
        print(ex)
        assert False

    with open('tests/chroot/home/testinput', 'r') as fd:
        assert len(fd.read()) > 1

def test_IO_read(FileTCP_testing, IO_Ctl_fixture):
    ftcp = FileTCP_testing
    ftcp.read_tcp_struct()
    elist = ftcp.get_entries()
    for entry in elist:
        entry.resolve_country() # waiting for pull
    try:
        IO_Ctl_fixture.write_to_file(elist)
    except Exception as ex:
        print(ex)
        assert False

    with open('tests/chroot/home/testinput', 'r') as fd:
        assert len(fd.read()) > 1

    try:
        fl = IO_Ctl_fixture.read_from_file()
        assert isinstance(fl, list)
        for item in fl:
            assert isinstance(item, EntryTCP)
    except Exception as ex:
        print(ex)
        assert False
