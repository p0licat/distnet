
import re


from src.hex_manip import hex_dict


def test_hex_dict():
    m_ptr = re.compile(r'[0-9a-fA-F]')

    hd = hex_dict()

    for i in hd.keys():
        assert m_ptr.match(i) # NoneType on fail
