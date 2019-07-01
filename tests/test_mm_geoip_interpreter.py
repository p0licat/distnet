"""
    Tests for mmdb csv format interpreter and location getter.
"""

import os
import sys
import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../distnet"))

from utils.mm_geoip_interpreter import GeoIP_Controller

@pytest.fixture
def GeoIP_Controller_Instance():
    return GeoIP_Controller()

# def test_GeoIP_Controller_Init_dbgout(GeoIP_Controller_Instance):
#     geoip_c = GeoIP_Controller_Instance
#     assert False


def test_GeoIP_Controller_Init(GeoIP_Controller_Instance):
    geoip_c = GeoIP_Controller_Instance
    assert True

def test_GeoIP_Controller_search(GeoIP_Controller_Instance):
    geoip_c = GeoIP_Controller_Instance
    assert geoip_c.search_CIDR_location('46.17.16.3') != None
    assert geoip_c.search_CIDR_location('46.17.16.3') == 'NO'
