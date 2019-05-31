
import re


from src.hex_manip import hex_dict, int_from_string, ip_from_hex, port_from_hex
from src.tcp_structs_exceptions import HexadecimalStringFormatError, \
    HexadecimalIpFormatError, HexadecimalPortFormatError

def test_hex_dict():
    m_ptr = re.compile(r'[0-9a-fA-F]')

    hd = hex_dict()

    for i in hd.keys():
        assert m_ptr.match(i) # NoneType on fail

def test_int_from_string():
    hex_strings = {"AF": 175, "1A": 26, "F3": 243}

    for string in hex_strings.keys():
        i_val = int_from_string(string)
        assert i_val == hex_strings[string]

    try:
        int_from_string("FG")
        assert False
    except HexadecimalStringFormatError:
        assert True

def test_ip_from_hex():
    m_ptr = re.compile(r'[0-9a-fA-F\.]')
    valid_ip_list = ["AABBCCDD", "F100A8C0"]
    bad_ip_list = ["AABBCCGX", "AAA"]

    for item in valid_ip_list:
        ip = ip_from_hex(item)
        assert isinstance(ip, str)
        for s_chr in ip:
            assert m_ptr.match(s_chr)


    for item in bad_ip_list:
        try:
            ip_from_hex(item)
            assert False
        except HexadecimalIpFormatError:
            assert True

    valid_dict = {"AABBCCDD": "221.204.187.170", "F100A8C0": "192.168.0.241"}
    for v_ip in valid_dict.keys():
        conv_ip = ip_from_hex(v_ip)
        assert conv_ip == valid_dict[v_ip]

def test_port_from_hex():
    m_ptr = re.compile(r'[0-9a-fA-F]')
    valid_port_list = ["AAAA", "C040"]
    bad_port_list = ["C040C040", "F100A8C0"]

    for item in valid_port_list:
        port = port_from_hex(item)
        assert isinstance(port, str)
        for s_chr in port:
            assert m_ptr.match(s_chr)

    for item in bad_port_list:
        try:
            port_from_hex(item)
            assert False
        except HexadecimalPortFormatError:
            assert True

    valid_dict = {"AAAA": 43690, "C040": 49216}
    for v_port in valid_dict.keys():
        conv_port = port_from_hex(v_port)
        try:
            int(conv_port)
            assert True
        except:
            assert False
        assert int(conv_port) == valid_dict[v_port]
