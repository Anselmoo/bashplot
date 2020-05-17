#!/usr/bin/env python
"""Bashplot: Instant data plotting from the terminal into the terminal."""


######################################################
#
# bashplot - instant plotting via the command line
# written by Anselm Hahn (Anselm.Hahn@gmail.com)
# inspired by Benjamin Gleitzman (gleitz@mit.edu)
#
######################################################

import argparse
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


def log(msg, mode=None):
    """Print messages to display.

    Parameters
    ----------
    msg : str
        Message to print to the terminal.
    mode : int, optional
        If mode is activated, message becomes an error message.
    """
    if mode:
        print(f"[ERROR] {msg}")
    else:
        print(msg)


def load_data(fname, args):
    """Load data via np.genfromtxt.

    Parameters
    ----------
    fname : str
        Filename to load via np.genfromtxt.
    args : dict
        Dictionary of the keywords and values from the parser.

    Returns
    -------
    data : float-array
        Returns a 2D-Numpy-array with `dtype=float`.
    """
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


def plot_plot(fig, x, Y, label):
    """Make the plot-figures.

    plot_plot() is generating a single- or multi-plot by recursiving calling plot().

    Parameters
    ----------
    fig : class
        Figure class for the terminal plot
    x : float-array
        1D-Numpy-array with the float column x-values.
    Y : float-array
        1D- or 2D-Numpy-array with the float column Y-values.
    label : str
        The label of the plot(s) is the current filename.
    
    Returns
    -------
    fig :  class
        Updated figure class for the terminal plot 
    plot_plot() : function
        Returns the function itself for a smaller (n-1) float-array (Y) until it is an
        1D-array.
    """
    if Y.shape[1] == 1:
        fig.plot(x, Y[:, 0], label=label)
        return fig
    else:
        fig.plot(x, Y[:, 0], label=label)
        return plot_plot(fig, x, Y[:, 1:], label=label)


def plot_scatter(fig, x, Y, label):
    """Make the scatter-figures.

    plot_scatter() is generating a single- or multi-plot by recursiving calling
    scatter().

    Parameters
    ----------
    fig : class
        Figure class for the terminal plot
    x : float-array
        1D-Numpy-array with the float column x-values.
    Y : float-array
        1D- or 2D-Numpy-array with the float column Y-values.
    label : str
        The label of the scatter-plot(s) is the current filename.
    
    Returns
    -------
    fig :  class
        Updated figure class for the terminal plot 
    plot_scatter() : function
        Returns the function itself for a smaller (n-1) float-array (Y) until it is an
        1D-array.
    """
    if Y.shape[1] == 1:
        fig.scatter(x, Y[:, 0], label=label)
        return fig
    else:
        fig.scatter(x, Y[:, 0], label=label)
        return plot_plot(fig, x, Y[:, 1:], label=label)


def plot(data, args, label):
    """Generate the plots as classical or scatter plots.

    plot() is generating the classical or scatter plots according to the arguments 
    `args`.

    Parameters
    ----------
    data : float-array
        2D-Numpy-array with `dtype=float`.
    args : dict
        Dictionary of the keywords and values from the parser.
    label : str
        The label of the scatter-plot(s) is the current filename.
    """
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
            fig = plot_scatter(fig, x=x, Y=y, label=label)
        else:
            fig = plot_plot(fig, x=x, Y=y, label=label)

        if args["legend"]:
            log(fig.show(legend=True))
        else:
            log(fig.show(legend=False))
    except IndexError:
        log(f"corrupted data in {label}", mode=1)
        sys.exit(1)


def bashplot(fnames, args):
    """bashplot.
    
    bashplot() is plotting each file independently according to the args. For a
    filename list >1, bashplot() is calling itself again by reducing the list by
    the value of -1.
    
    Parameters
    ----------
    fnames : str-list
        List of the filename(s); is always a list even if single value included.
    args : dict
        Dictionary of the keywords and values from the parser.

    Returns
    -------
    bashplot() : function
        Returns the function itself for smaller (n-1) list of filenames (fnames).
    """
    if len(fnames) == 1:
        data = load_data(fname=Path(fnames[0]), args=args)
        plot(data, args, label=fnames[0])
    else:
        data = load_data(fname=Path(fnames[0]), args=args)
        plot(data, args, label=fnames[0])
        return bashplot(fnames[1:], args)


def get_args(opt=None):
    """Get the parser arguments from the command line.
    
    Parameters
    ----------
    opt : dict, optional
        Optional Dictionary for modifying the parser arguments; default is None.
    
    Returns
    -------
    args : dict
        Dictionary of the keywords and values from the parser.
    """
    parser = argparse.ArgumentParser(
        description=("Instant data plotting from the terminal into the terminal")
    )
    # Arguments for loading the data
    parser.add_argument(
        "infile", nargs="*", type=str, help="load data file(s) as ASCII"
    )

    parser.add_argument(
        "-cm",
        "--comments",
        help=(
            "define the character to indicate the start of the document; "
            "default is None"
        ),
        default=None,
        type=str,
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        help=(
            "define the type of deilimiter; default is any consecutive " "'whitespace'"
        ),
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
            "define the mimimum and maximum x-range of the plot; default is the "
            "automatic generated minimum and the maximum of the data, but can be "
            "replaced by any float-values."
        ),
        default=None,
        nargs=2,
        type=float,
    )
    parser.add_argument(
        "-y",
        "--y_limits",
        help=(
            "define the mimimum and maximum y-range of the plot; default is the "
            "automatic generated minimum and the maximum of the data, but can be "
            "replaced by any float-values."
        ),
        default=None,
        nargs=2,
        type=float,
    )
    parser.add_argument(
        "-sc",
        "--scatter",
        help=("replaced regular plot by scatter plot"),
        action="store_true",
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
    if opt:
        for item, value in opt.items():
            args[item] = value
    return args


def command_line_runner():
    """Run bashplot() via command line."""
    args = get_args()

    if args["version"]:
        log(__version__)

    if not args["infile"]:
        log("Missing input file(s)!", mode=1)
        return
    
    fnames = args["infile"]
    bashplot(fnames, args)


if __name__ == "__main__":
    command_line_runner()
