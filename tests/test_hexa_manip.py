
import re


from src.hexa_manip import hexa_dict


def test_hexa_dict():
    m_ptr = re.compile(r'[0-9a-fA-F]')

    hd = hexa_dict()

    for i in hd.keys():
        assert m_ptr.match(i) # NoneType on fail
