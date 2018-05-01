#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2017-09-27


import unittest
import os
import glob
import pandas as pd
from sphere import sphere_estimate
from sphere.sphere_utils import get_logger


class SphereEstimateTest(unittest.TestCase):
    logger = get_logger(__name__)

    def setUp(self):
        self.maxDiff = None
        d_dir = os.path.dirname(__file__) + "/data/test_sphere_estimate"
        file_path = "{0}/input_*.tsv".format(d_dir)
        self.__input = glob.glob(file_path)
        self.__output = d_dir + "/output.tsv"
        self.__output_model = d_dir + "/model.pkl"
        self.__output_fit = d_dir + "/fit.pkl"
        self.__output_ll = d_dir + "/log_lik.tsv"

    def tearDown(self):
        if os.path.exists(self.__output):
            os.remove(self.__output)
        if os.path.exists(self.__output_model):
            os.remove(self.__output_model)
        if os.path.exists(self.__output_fit):
            os.remove(self.__output_fit)
        if os.path.exists(self.__output_ll):
            os.remove(self.__output_ll)

    def test_sphere_estimate_main_linearcardioid_multiple(self):
        args = {
            "depth_file_path": self.__input,
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "linearcardioid",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_linearcardioid_single(self):
        args = {
            "depth_file_path": [self.__input[0]],
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "linearcardioid",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_cardioid_multiple(self):
        args = {
            "depth_file_path": self.__input,
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "cardioid",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_cardioid_single(self):
        args = {
            "depth_file_path": [self.__input[0]],
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "cardioid",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_wrappedcauchy_multiple(self):
        args = {
            "depth_file_path": self.__input,
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "wrappedcauchy",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_wrappedcauchy_single(self):
        args = {
            "depth_file_path": [self.__input[0]],
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "wrappedcauchy",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_sswrappedcauchy_multiple(self):
        args = {
            "depth_file_path": self.__input,
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "sswrappedcauchy",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_sswrappedcauchy_single(self):
        args = {
            "depth_file_path": [self.__input[0]],
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "sswrappedcauchy",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_vonmises_multiple(self):
        args = {
            "depth_file_path": self.__input,
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "vonmises",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_vonmises_single(self):
        args = {
            "depth_file_path": [self.__input[0]],
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "vonmises",
            "M": "sampling",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_argument_parse(self):
        argv_str = """{0} {1} -pmd {2} -fod {3}
                       -lld {4} -sc 1 -si 50 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_model,
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        args_answer = {
            "depth_file_path": [self.__input[0]],
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "vonmises",
            "M": "sampling",
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None
        }
        self.assertDictEqual(args, args_answer)

    def test_sphere_estimate_command_sampling(self):
        argv_str = """{0} {1} -pmd {2} -fod {3} -lld {4}
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_model,
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_vonmises_multiple_optimizing(self):
        args = {
            "depth_file_path": self.__input,
            "output_dest": self.__output,
            "pmd": self.__output_model,
            "pmp": None,
            "m": "vonmises",
            "M": "optimizing",
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_optimizing(self):
        argv_str = """{0} {1} -M optimizing -m vonmises -ff""".format(
            self.__output,
            self.__input[0],
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def assertStanConvergence(self, args):
        df = pd.read_csv(args["output_dest"],
                         sep="\t",
                         index_col=0)
        n_not_converted = len(df[df["Rhat"] >= 1.1])
        self.assertEqual(n_not_converted, 0)


if __name__ == '__main__':
    unittest.main()
