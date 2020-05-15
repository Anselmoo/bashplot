#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import sys

import numpy as np
import plotille as plt

try:
    from . import __version__
except ImportError:
    from __init__ import __version__

if sys.version < "3":
    print("Unsupported Python Version (version < 3)!")
    sys.exit(1)


def log(arg, mode=None):

    if mode:
        print(f"[ERROR] {arg}")
    else:
        print(arg)


def load_data(fname, args):

    data = np.genfromtxt(
        fname,
        dtype=np.float,
        comments=args["comments"],
        delimiter=args["delimiter"],
        skip_header=args["skip_header"],
        skip_footer=args["skip_footer"],
        usecols=args["usecols"],
    )
    return data


def _plot(fig, x, Y, label):
    if Y.shape[1] == 1:
        fig.plot(x, Y[:, 0], label=label)
        return fig
    else:
        fig.plot(x, Y[:, 0], label=label)
        return _plot(fig, x, Y[:, 1:], label=label)

def _scatter(fig, x, Y, label):
    if Y.shape[1] == 1:
        fig.scatter(x, Y[:, 0], label=label)
        return fig
    else:
        fig.scatter(x, Y[:, 0], label=label)
        return _plot(fig, x, Y[:, 1:], label=label)

def plot(data, args, label):

    fig = plt.Figure()
    fig.widht = args["size"][0]
    fig.height = args["size"][1]
    try:

        if args["x_limits"]:
            fig.set_x_limits(min_=args["x_limits"][0], max_=args["x_limits"][1])
        else:
            fig.set_x_limits(min_=np.min(data[:, 0]), max_=np.max(data[:, 0]))

        if args["y_limits"]:
            fig.set_y_limits(min_=args["y_limits"][0], max_=args["y_limits"][1])
        else:
            fig.set_y_limits(min_=np.min(data[:, 1]), max_=np.max(data[:, 1]))

        if args["color"]:
            fig.color_mode = "rgb"

        x = data[:, 0]
        y = data[:, 1:]

        if args["scatter"]:
            fig = _scatter(fig, x=x, Y=y, label=label)
        
        else:
            fig = _plot(fig, x=x, Y=y, label=label)

        if args["legend"]:
            print(fig.show(legend=True))
        else:
           print(fig.show(legend=False)) 
    except IndexError:
        log(f"corrupted data in {label}", mode=1)
        sys.exit(1)


def bashplot(fnames, args):

    if len(fnames) == 1:
        data = load_data(fname=Path(fnames[0]), args=args)
        plot(data, args, label=fnames[0])
    else:
        data = load_data(fname=Path(fnames[0]), args=args)
        plot(data, args, label=fnames[0])
        return bashplot(fnames[1:], args)


def get_parser():
    parser = argparse.ArgumentParser(
        description=("Instant data plotting from the terminal into the terminal")
    )
    # Arguments for loading the data
    parser.add_argument(
        "infile", nargs="*", type=str, help="load data file(s) as ASCII"
    )
    parser.add_argument("-p", "--pos", help="plot", default=1, type=int)

    parser.add_argument(
        "-cm",
        "--comments",
        help=(
            "define the character to indicate the start of the document; default is None"
        ),
        default=None,
        type=str,
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        help=("define the type of deilimiter; default is any consecutive 'whitespace'"),
        default=None,
        type=str,
    )
    parser.add_argument(
        "-skh",
        "--skip_header",
        help=(
            "define the number of skipped rows from the beginning of the document; "
            "default is 0"
        ),
        default=0,
        type=int,
    )
    parser.add_argument(
        "-skf",
        "--skip_footer",
        help=(
            "define the number of skipped rows from the end of the document; "
            "default is 0"
        ),
        default=0,
        type=int,
    )
    parser.add_argument(
        "-col",
        "--usecols",
        help=(
            "define the pair of x- and y-columns for the data plot; default is None. "
            "This  means all available will be loaded; otherwise tip a series of "
            "columns started with 0 like 0, 1, 4"
        ),
        default=None,
        nargs=2,
        type=int,
    )
    # Arguments for plotting the data
    parser.add_argument(
        "-sz",
        "--size",
        help=(
            "define the width and heights of the plots; default is width = 60 and the "
            "heights = 40. The values have to be int-values."
        ),
        default=[60, 40],
        nargs=2,
        type=int,
    )
    parser.add_argument(
        "-x",
        "--x_limits",
        help=(
            "define the mimimum and maximum x-range of the plot; default is the automatic "
            "generated minimum and the maximum of the data, but can be replaced by any "
            "float-values."
        ),
        default=None,
        nargs=2,
        type=float,
    )
    parser.add_argument(
        "-y",
        "--y_limits",
        help=(
            "define the mimimum and maximum y-range of the plot; default is the automatic "
            "generated minimum and the maximum of the data, but can be replaced by any "
            "float-values."
        ),
        default=None,
        nargs=2,
        type=float,
    )
    parser.add_argument(
        "-sc", "--scatter", help=("replaced regular plot by scatter plot"), action="store_true"
    )
    parser.add_argument(
        "-c", "--color", help=("enable RGB colorized the plots"), action="store_true"
    )
    parser.add_argument(
        "-l", "--legend", help=("enable the legend of the plots"), action="store_false"
    )
    parser.add_argument(
        "-v",
        "--version",
        help=("displays the current version of bathchplot"),
        action="store_true",
    )
    args = vars(parser.parse_args())
    return args


def command_line_runner():
    args = get_parser()

    if args["version"]:
        log(__version__)

    if not args["infile"]:
        log("Missing input file(s)!", mode=1)
        return
    else:
        fnames = args["infile"]
        bashplot(fnames, args)


if __name__ == "__main__":
    command_line_runner()
