import os
import sys
import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../distnet"))

from network_controller import resolve_hostname, resolve_location

def test_invalid_resolve_hostname():
    with pytest.raises(Exception) as exception_info:
        resolve_hostname('notavalidaddress.right')
    assert exception_info.typename == "gaierror"

def test_invalid_resolve_location():
    assert resolve_location('whatastrangehostname') == 'whatastrangehostname'

def test_resolve_location_tldstring():
    assert resolve_location('whatastrangehostname.uk') == 'uk'

def test_resolve_location_us():
    assert resolve_location('google.com') == 'us'
