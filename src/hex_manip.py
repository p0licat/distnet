"""
    Module contains classes and methods for hexadecimal conversions between str,
    hexadecimal, and formats found in /proc/net/ files in Linux.
"""

from tcp_structs_exceptions import EntryTCP_InitError, HexadecimalIpFormatError, \
    HexadecimalPortFormatError, EntryTCP_FormatError

def hexa_dict():
    h_dict = {}
    ind = 0
    for i in    [str(i) for i in range(10)] + \
                [chr(0x61 + i) for i in range(6)] + \
                [chr(0x41 + i) for i in range(6)]:
        h_dict[i] = ind if ind <= 15 else ind - 6
        ind += 1

    return h_dict

def int_from_string(hex_string):

    hd = hexa_dict()
    value = 0
    i = 0
    for char in hex_string[::-1]:
        val = None
        try:
            val = hd[char]
        except KeyError as ke:
            raise HexadecimalStringFormatError("Not a hex string.", "String contained: {0}".format(char))
        value += pow(16, i) * val
        i += 1

    return value


def ip_from_hex(string):
    h_dict = hexa_dict()

    rval = ""
    if len(string) != 8:
        raise HexadecimalIpFormatError('Not a valid IPv4 string.', string)

    s = string[::-1]
    o = []
    while s:
        o.append(s[:2])
        s = s[2:]
    for pair in o:
        value = 0
        i = 0
        for h_char in pair:
            value += pow(16, i) * h_dict[h_char]
            i += 1
        rval += str(value) + '.'
    return rval.rstrip('.')

def port_from_hex(string):
    h_dict = hexa_dict()

    rval = 0
    if len(string) != 4:
         raise HexadecimalPortFormatError('Not a valid hexadeimal port string.', string)

    # TODO: test before next todo
    # TODO: refactor into *_from_ -> from() : 1. check 2. call int_from
    s = string[::-1]

    i = 0
    for h_char in s:
        rval += pow(16, i) * h_dict[h_char]
        i += 1
    return str(rval)
