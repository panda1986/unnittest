# -*- coding: utf-8 -*-

import unittest
from test_playout import TestVodResource
from HTMLTestRunner import HTMLTestRunner

if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [TestVodResource("test_put"), TestVodResource("test_delete")]
    suite.addTests(tests)

    '''with open("report.html", "w") as f:
        runner = HTMLTestRunner(stream=f, verbosity=2, title="TestPlayout", description="test vode resource")
        runner.run(suite)
    '''
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)