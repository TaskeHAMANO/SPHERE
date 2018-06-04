#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2017-09-27


import unittest
import os
import filecmp
from sphere import sphere_filter
from sphere.sphere_utils import get_logger


class SphereFilterTest(unittest.TestCase):
    logger = get_logger(__name__)

    def setUp(self):
        self.maxDiff = None
        d_dir = os.path.dirname(__file__) + "/data/test_sphere_filter"
        self.__input1 = d_dir + "/input1.tsv"
        self.__input2 = d_dir + "/input2.tsv"
        self.__input3 = d_dir + "/input3.tsv"
        self.__output = d_dir + "/output.tsv"
        self.__answer2 = d_dir + "/answer2.tsv"
        self.__answer3 = d_dir + "/answer3.tsv"

    def tearDown(self):
        if os.path.exists(self.__output):
            os.remove(self.__output)

    def test_sphere_filter_main(self):
        args = {
            "depth_file_path": self.__input1,
            "output_dest": self.__output,
            "s": 10,
            "w": 10
        }
        sphere_filter.main(args, SphereFilterTest.logger)

    def test_sphere_filter_main_non_devidable(self):
        args = {
            "depth_file_path": self.__input1,
            "output_dest": self.__output,
            "s": 7,
            "w": 11
        }
        sphere_filter.main(args, SphereFilterTest.logger)

    def test_sphere_filter_command1(self):
        argv_str = "{0} {1} -s 10 -w 10".format(self.__output, self.__input1)
        argv = argv_str.split()
        args = sphere_filter.argument_parse(argv)
        sphere_filter.main(args, SphereFilterTest.logger)

    def test_sphere_filter_command2(self):
        argv_str = "{0} {1} -s 1 -w 6".format(self.__output, self.__input2)
        argv = argv_str.split()
        args = sphere_filter.argument_parse(argv)
        sphere_filter.main(args, SphereFilterTest.logger)
        result = filecmp.cmp(self.__output, self.__answer2)
        self.assertTrue(result)

    def test_sphere_filter_command3(self):
        argv_str = "{0} {1} -s 2 -w 3".format(self.__output, self.__input3)
        argv = argv_str.split()
        args = sphere_filter.argument_parse(argv)
        sphere_filter.main(args, SphereFilterTest.logger)
        result = filecmp.cmp(self.__output, self.__answer3)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
