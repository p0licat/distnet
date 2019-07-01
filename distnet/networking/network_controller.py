"""
    Network related operations.
    TODO: master class with static methods and os checks for connectivity
"""

import socket
import whois
import time

from utils.mm_geoip_interpreter import GeoIP_Controller

def resolve_hostname(dest_ip):
    """
        Try to query hostname.
    """

    try:
        return str(socket.gethostbyaddr(dest_ip)[0])
    except socket.herror as he:
        return str("")
    except socket.gaierror as ge:
        raise ge

def resolve_location(hostname, ip=None, verbose=False):
    """
        Try to assign a location to a hostname.
    """
    whois_response = None
    geoip_response = None # TODO: geoip
    tld_string = None

    whois_countries = dict()
    rloc = None

    # geoip determination
    if (ip):
        if verbose == True:
            print("Trying to lookup geoip with {0}".format(ip))

        gc = GeoIP_Controller()
        geoip_response = gc.search_CIDR_location(ip)
        if geoip_response is not None:
            geoip_response = geoip_response.lower()

    # DNS query
    if hostname != "":
        for i in range(3):
            if verbose:
                if verbose == True:
                    print("Attempting to resolve location: "  + hostname)

            try:
                whois_response = whois.whois(hostname)
            except Exception as ex:
                #print(ex)
                continue

            tdata = whois_response
            try:
                tdata = tdata.text
            except AttributeError as ae:
                continue


            cdata = []
            for i in tdata.split('\n'):
                if 'Registrant Country:' in i:
                    ccode = i.split(' ')[2].rstrip('\r').rstrip('\n').rstrip()
                    ccode = ccode.lower()
                    cdata.append(ccode)
                    whois_countries[ccode] = 1 if ccode not in whois_countries else whois_countries[ccode] + 1

            break

    # fallback url determination
    tld_string = hostname.split('.')[-1].rstrip().lstrip('.')

    # priorities are whois > geoip > url
    if len(whois_countries.keys()) != 0:
        rloc = list(whois_countries.keys())[0]
    elif geoip_response != None:
       rloc = geoip_response
    elif tld_string != None:
        return tld_string

    if verbose == True:
        print(rloc)

    return rloc
