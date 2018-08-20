"""
Testfile for get_weather.py
"""

import get_weather as gw
from get_weather import requests_cache
import os


def test_request_data(tmpdir):
    p = str(tmpdir)
    requests_cache.install_cache(os.path.join(p, 'test_cache'),
                                 expire_after=300)
    data = gw.request_data('Portland')
    data2 = gw.request_data(97239)
    assert isinstance(data, dict)
    assert isinstance(data2, dict)
    assert os.path.exists('test_cache.sqlite')
    requests_cache.uninstall_cache()


def test_temp_conversion():
    assert gw.temp_conversion(273) == (0, 32)
