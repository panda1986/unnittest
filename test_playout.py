# -*- coding: utf-8 -*-

import unittest
import bravo_utility
from bravo_constants import Errors

playout_host_port = "192.168.3.147:2047"
open_key = "BSz1s7lP71N4BCdEXxLgUQ=="

'''
ref: http://192.168.1.230:3000/bravo_dev/dev_docs/src/master/products/playout/playout_resources_api.md
'''
vode_resource_api = '/api/v2.0/playout/resources/vod'

def get_resource_vod():
    url = 'http://%s%s?page=%d&per_page=%d&token=%s' % (playout_host_port, vode_resource_api, 1, 10, open_key)
    (code, data, msg) = bravo_utility.bravo_http_get(url)
    if not Errors.is_success(code):
        print msg
        return (code, None)
    return (code, data["videos"])

def get_resource_vod_by_id(id):
    url = 'http://%s%s?id=%s&token=%s' % (playout_host_port, vode_resource_api, id, open_key)
    (code, data, msg) = bravo_utility.bravo_http_get(url)
    if not Errors.is_success(code):
        print msg
        return (code, None)
    return (code, data["videos"])

class TestVodResource(unittest.TestCase):

    def test_put(self):
        (code, videos) = get_resource_vod()
        self.assertTrue(Errors.is_success(code))
        if len(videos) > 0:
            resource = videos[0]
            self.assertIn("video_id", resource)
            self.assertIn("video_name", resource)
            # update name
            ori_resource_name = resource["video_name"]
            new_name = "test_test"
            # example: http://192.168.3.147:2047/api/v2.0/playout/resources/vod?id=1503011327621383721
            url = "http://%s%s?id=%s&token=%s" % (playout_host_port, vode_resource_api, resource["video_id"], open_key)
            body = {"name": new_name}
            (code, data, msg) = bravo_utility.bravo_http_post(url, bravo_utility.json_dumps(body), method="PUT")
            self.assertTrue(Errors.is_success(code))
            # 目前还不支持按video_id查询单个素材, 需支持后进行验证video_name是否修改成功


    def test_delete(self):
        (code, videos) = get_resource_vod()
        self.assertTrue(Errors.is_success(code))
        if len(videos) > 0:
            resource = videos[0]
            self.assertIn("video_id", resource)
            # example: http://192.168.3.147:2047/api/v2.0/playout/resources/vod
            url = "http://%s%s?token=%s" % (playout_host_port, vode_resource_api, open_key)
            ids = {
                "ids": [resource["video_id"]]
            }
            (code, data, msg) = bravo_utility.bravo_http_post(url, bravo_utility.json_dumps(ids), method="DELETE")
            self.assertTrue(Errors.is_success(code))
            # 目前还不支持按video_id查询单个素材, 需支持后进行验证video_name是否已删除
