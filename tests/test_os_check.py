
from src.os_check import os_filesystem_check

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
