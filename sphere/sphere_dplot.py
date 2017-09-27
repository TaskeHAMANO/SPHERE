#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2017-09-26

import argparse
import matplotlib.pyplot as plt
import numpy as np
from logging import getLogger, DEBUG, Formatter, StreamHandler
from matplotlib import gridspec
from sphere.sphere_utils import load_depth_file
from sphere.sphere_utils import compress_depth


def get_logger():
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    log_fmt = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
    formatter = Formatter(log_fmt)
    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def argument_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("depth_file_path",
                        type=str,
                        help="file path of coverage depth")
    parser.add_argument("output_file_dest",
                        type=str,
                        help="destination of output file")
    parser.add_argument("-np", "--npetal",
                        dest="np",
                        type=int,
                        nargs="?",
                        default=30,
                        help="Number of petal in rose diagram (default: 30)")
    parser.add_argument("-fs", "--fontsize",
                        dest="fs",
                        type=int,
                        nargs="?",
                        default=30,
                        help="Font size of figure (default: 18)")
    args = parser.parse_args()
    return vars(args)


def main(args, logger):
    fs = args["fs"]
    df = load_depth_file(args["depth_file_path"])
    x = df["position"].values
    y = df["depth"].values
    I = len(df)
    t1 = np.arange(0, 2*np.pi, 2*np.pi/args["np"])
    t2 = np.arange(0, 2*np.pi, 2*np.pi/I)
    y_f = compress_depth(y, I, args["np"], "floor")
    width = 2 * np.pi / (args["np"]+10)

    fig = plt.figure(figsize=(20, 20))
    gs = gridspec.GridSpec(2, 2)

    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(x, y)
    ax1.set_xlabel("Genomic position", fontsize=fs)
    ax1.set_ylabel("Coverage depth", fontsize=fs)
    ax1.tick_params(labelsize=fs)

    ax2 = fig.add_subplot(gs[1, 0], projection="polar")
    ax2.bar(t1, y_f, width=width)
    ax2.set_theta_zero_location("N")
    ax2.set_xticks(np.arange(0, 360, 360/6) / 360 * 2 * np.pi)
    ax2.set_xticklabels(np.arange(0, I, I/6, dtype=int))
    ax2.tick_params(labelsize=fs)

    ax3 = fig.add_subplot(gs[1, 1], projection="polar")
    ax3.plot(t2, y)
    ax3.set_theta_zero_location("N")
    ax3.set_xticks(np.arange(0, 360, 360/6) / 360 * 2 * np.pi)
    ax3.set_xticklabels(np.arange(0, I, I/6, dtype=int))
    ax3.tick_params(labelsize=fs)

    plt.savefig(args["output_file_dest"])


if __name__ == '__main__':
    main(argument_parse(), get_logger())
