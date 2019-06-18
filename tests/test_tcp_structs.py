
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../distnet'))

from tcp_structs import C_STATE
from tcp_file_entry import EntryTCP
from hex_manip import int_from_string


def test_c_state():
    """
        Range test for bounded values.
    """
    assert C_STATE.close == 0x7
    assert C_STATE.check_bounds(0x7) == C_STATE.close

    # full range
    for value in range(0x1, 0xB + 1):
        try:
            C_STATE.check_bounds(value)
            assert True
        except:
            assert False


    try:
        C_STATE.check_bounds(0xFF)
        assert False
    except ValueError as ex:
        assert True

    # full range
    for value in range(0x1, 0xB + 1):
        try:
            v = C_STATE.check_bounds(value)
            assert C_STATE.hex_from_string(C_STATE.string_from_hex(v)) is not None
            assert True
        except Exception as ex:
            print(ex)
            assert False

    # lower bound
    try:
        C_STATE.check_bounds(0x0)
        assert False
    except ValueError as ex:
        assert True

    try:
        C_STATE.check_bounds(0x1)
        assert True
    except ValueError as ex:
        assert False


    # upper bound
    try:
        C_STATE.check_bounds(0xB)
        assert True
    except ValueError as ex:
        assert False

    try:
        C_STATE.check_bounds(0xC)
        assert False
    except ValueError as ex:
        assert True

    try:
        C_STATE.hex_from_string(13)
        assert False
    except TypeError:
        assert True

    try:
        C_STATE.hex_from_string("other_value")
        assert True
    except: # TODO
        assert False


    try:
        assert C_STATE.hex_from_string("established") == 1
        assert True
    except: # TODO
        assert False
