
import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../distnet"))

from os_check import os_filesystem_check

def test_os_filesystem_check_empty():
    try:
        os_filesystem_check()
        assert False
    except TypeError as te:
        assert True

def test_os_filesystem_check_Passing():
    assert os_filesystem_check(directory='/proc/net///', files_list=[
        '/tcp',
        '//tcp6',
        'udp',
        'udp6'
    ], filetype_pattern=': empty$') == True

def test_os_filesystem_check_not_existing():
    # is not dir
    assert os_filesystem_check(directory='/proc/exists/', files_list=[
        'tcp',
        'udp'
    ], filetype_pattern=': empty$') == False

def test_os_filesystem_check_existing_file():
    # is not dir
    assert os_filesystem_check(directory='/proc/uptime', files_list=[
        'tcp',
        'udp'
    ], filetype_pattern=': empty$') == False

    assert os_filesystem_check(directory='/proc/uptime/', files_list=[
        'tcp',
        'udp'
    ], filetype_pattern=': empty$') == False


def test_os_filesystem_check_existing_files_and_dirs():
    assert os_filesystem_check(directory='/proc/net', files_list=[
        'tcp12',    # should not exist
        'udp12',    # should not exist
        'stat'      # stat is a dir under /proc/net
    ], filetype_pattern=': empty$') == False

def test_os_filesystem_check_existing_PopenErr():
    assert os_filesystem_check(directory='tests/chroot/proc/net', \
    files_list = [
        'notaccessible'
    ], filetype_pattern=':empty $') == False
