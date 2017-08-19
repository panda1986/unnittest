# -*- coding: utf-8 -*-

import unittest
from test_playout import TestVodResource
from HTMLTestRunner import HTMLTestRunner

if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [TestVodResource("test_get")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)