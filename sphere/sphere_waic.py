#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2017-10-04

import argparse
import os
import pandas as pd
from sphere.stan_utils import load_log_lik
from sphere.stan_utils import get_waic
from sphere.sphere_utils import get_logger
from sphere.sphere_utils import load_multiple_depth_file


def argument_parse(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dest",
                        type=str)
    parser.add_argument("log_lik_files",
                        nargs="+",
                        type=str)
    parser.add_argument("-t", "--type",
                        dest="t",
                        nargs="?",
                        default="both",
                        choices=["original", "bda3", "both"],
                        type=str)
    parser.add_argument("-d", "--depth",
                        dest="d",
                        nargs="*",
                        default=None,
                        type=str)
    args = parser.parse_args(argv)
    return vars(args)


def main(args, logger):
    results = []
    if args["d"] is not None:
        ddf = load_multiple_depth_file(args["d"])
        ddf = ddf[ddf["depth"] != 0]
        depth = ddf["depth"].values
    else:
        depth = None

    for f in args["log_lik_files"]:
        name = os.path.basename(f)
        log_lik = load_log_lik(f)
        if args["t"] != "both":
            waic = get_waic(log_lik, depth, args["t"])
            results.append({
                "file_name": name,
                "file_path": f,
                "waic_{0}".format(args["t"]): waic
            })
        else:
            waic_original = get_waic(log_lik, depth, "original")
            waic_bda3 = get_waic(log_lik, depth, "bda3")
            results.append({
                "file_name": name,
                "file_path": f,
                "waic_original": waic_original,
                "waic_bda3": waic_bda3
            })

    df = pd.DataFrame(results)
    df = df.set_index("file_name")
    df.to_csv(args["output_dest"], sep="\t")


if __name__ == '__main__':
    main(argument_parse(), get_logger(__name__))
