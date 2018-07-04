#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2017-09-27


import unittest
import os
import pandas as pd
from sphere import sphere_estimate
from sphere.sphere_utils import get_logger


class SphereEstimateTest(unittest.TestCase):
    logger = get_logger(__name__)

    def setUp(self):
        self.maxDiff = None
        d_dir = os.path.dirname(__file__) + "/data/test_sphere_estimate"
        self.__input = [d_dir+"/input_1.tsv", d_dir+"/input_2.tsv"]
        self.__input_mix = [d_dir + "/input_3.tsv"]
        self.__output = d_dir + "/output.tsv"
        self.__output_fit = d_dir + "/fit.pkl"
        self.__output_ll = d_dir + "/log_lik.tsv"

    def tearDown(self):
        if os.path.exists(self.__output):
            os.remove(self.__output)
        if os.path.exists(self.__output_fit):
            os.remove(self.__output_fit)
        if os.path.exists(self.__output_ll):
            os.remove(self.__output_ll)

    # main function test
    def test_sphere_estimate_main_cardioid_multiple(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": self.__input,
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "cardioid",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_cardioid_single(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "cardioid",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_wrappedcauchy_multiple(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": self.__input,
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "wrappedcauchy",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_wrappedcauchy_single(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "wrappedcauchy",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_sswrappedcauchy_multiple(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": self.__input,
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "sswrappedcauchy",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_sswrappedcauchy_single(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "sswrappedcauchy",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_vonmises_multiple(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": self.__input,
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "vonmises",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": None,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_vonmises_single(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "vonmises",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_main_vonmises_single_mix(self):
        args = {
            "output_dest": self.__output,
            "depth_file_path": self.__input_mix,
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "vonmises",
            "M": "sampling",
            "nmix": 2,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        sphere_estimate.main(args, SphereEstimateTest.logger)

    # argument parse evaluation
    def test_sphere_estimate_argument_parse_vonmises(self):
        argv_str = """{0} {1} -fod {2}
                       -lld {3} -sc 1 -si 50 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        args_answer = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": self.__output_fit,
            "lld": self.__output_ll,
            "m": "vonmises",
            "M": "sampling",
            "nmix": 1,
            "si": 50,
            "sw": 20,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": True,
            "p": None,
            "ll": False,
            "j": -1
        }
        self.assertDictEqual(args, args_answer)

    def test_sphere_estimate_argument_parse_cardioid(self):
        argv_str = """{0} {1} -m cardioid""".format(
            self.__output,
            self.__input[0]
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        args_answer = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": None,
            "lld": None,
            "m": "cardioid",
            "M": "sampling",
            "nmix": 1,
            "si": 3000,
            "sw": 1000,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": False,
            "p": None,
            "ll": False,
            "j": -1
        }
        self.assertDictEqual(args, args_answer)

    def test_sphere_estimate_argument_parse_wrappedcauchy(self):
        argv_str = """{0} {1} -m wrappedcauchy""".format(
            self.__output,
            self.__input[0]
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        args_answer = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": None,
            "lld": None,
            "m": "wrappedcauchy",
            "M": "sampling",
            "nmix": 1,
            "si": 3000,
            "sw": 1000,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": False,
            "p": None,
            "ll": False,
            "j": -1
        }
        self.assertDictEqual(args, args_answer)

    def test_sphere_estimate_argument_parse_sswrappedcauchy(self):
        argv_str = """{0} {1} -m sswrappedcauchy""".format(
            self.__output,
            self.__input[0]
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        args_answer = {
            "output_dest": self.__output,
            "depth_file_path": [self.__input[0]],
            "fod": None,
            "lld": None,
            "m": "sswrappedcauchy",
            "M": "sampling",
            "nmix": 1,
            "si": 3000,
            "sw": 1000,
            "sc": 1,
            "st": 1,
            "ss": 1234,
            "ff": False,
            "p": None,
            "ll": False,
            "j": -1
        }
        self.assertDictEqual(args, args_answer)

    # Full test for sampling
    def test_sphere_estimate_command_sampling_vm_single(self):
        argv_str = """{0} {1} -m vonmises -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_lc_single(self):
        argv_str = """{0} {1} -m linearcardioid -sc 1 -si 30 -sw 20
                      -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_ssvm_multiple(self):
        argv_str = """{0} {1} {2} -m ssvonmises -sc 1 -si 30 -sw 20
                      -ff""".format(
            self.__output,
            self.__input[0],
            self.__input[1],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_ssc_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m sscardioid
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_aec_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m aecardioid
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_aevm_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m aevonmises
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_aewc_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m aewrappedcauchy
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_sst_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m statespacetrigonal
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_ssl_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m statespacelinear
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_t_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m trigonal
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_sampling_l_single(self):
        argv_str = """{0} {1} -fod {2} -lld {3} -m linear
                       -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    # Check if log_lik destination is used but -ll frag is not used.
    def test_sphere_estimate_command_sampling_vm_single_ll_lld(self):
        argv_str = """{0} {1} -lld {2} -sc 1 -si 30 -sw 20 -ff""".format(
            self.__output,
            self.__input[0],
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    # Full test for optimizing
    def test_sphere_estimate_command_optimizing_ssvm_multiple(self):
        argv_str = """{0} {1} {2} -fod {2} -lld {3} -m ssvonmises -M optimizing
                      -ff""".format(
            self.__output,
            self.__input[0],
            self.__input[1],
            self.__output_fit,
            self.__output_ll
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_optimizing_vm_single(self):
        argv_str = """{0} {1} -M optimizing -m vonmises -ff""".format(
            self.__output,
            self.__input[0],
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_optimizing_vm_multiple(self):
        argv_str = """{0} {1} {2} -M optimizing -m vonmises -ff""".format(
            self.__output,
            self.__input[0],
            self.__input[1],
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_optimizing_lc_single(self):
        argv_str = """{0} {1} -M optimizing -m linearcardioid
                      -ff""".format(
            self.__output,
            self.__input[0],
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_optimizing_lc_multiple(self):
        argv_str = """{0} {1} {2} -M optimizing -m linearcardioid
                      -ff""".format(
            self.__output,
            self.__input[0],
            self.__input[1],
        )
        argv = argv_str.split()
        args = sphere_estimate.argument_parse(argv)
        sphere_estimate.main(args, SphereEstimateTest.logger)

    def test_sphere_estimate_command_optimizing_vm_single_mix(self):
        argv_str = """{0} {1} -M optimizing -m vonmises -nmix 2 -ff""".format(
            self.__output,
            self.__input_mix[0],
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
