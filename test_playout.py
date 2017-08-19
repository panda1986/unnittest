import unittest
import bravo_utility
from bravo_constants import Errors

playout_host_port = "192.168.3.147:2047"
open_key = "BSz1s7lP71N4BCdEXxLgUQ=="
vode_resource_api = '/api/v2.0/playout/resources/vod'

class TestVodResource(unittest.TestCase):
    def test_get(self):
        url = 'http://%s%s?page=%d&per_page=%d&token=%s' % (playout_host_port, vode_resource_api, 1, 10, open_key)
        (code, data, msg) = bravo_utility.bravo_http_get(url)
        self.assertTrue(Errors.is_success(code))

        if len(data) > 0:
            value = data[0]
            