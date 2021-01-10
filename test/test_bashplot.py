"""Test for basplot."""

from pathlib import Path
from unittest import mock

import pytest
import sample_generator

from bashplot import bashplot

sample_generator.generate()

print()

test_txt = list(Path.cwd().glob("test*.txt"))
test_dat = list(Path.cwd().glob("test*.dat"))
test_out = list(Path.cwd().glob("test*.out"))

args_1 = {
    "infile": test_txt,
    "comments": None,
    "delimiter": None,
    "skip_header": 0,
    "skip_footer": 0,
    "usecols": (0, 1),
    "size": [30, 20],
    "x_limits": None,
    "y_limits": None,
    "scatter": False,
    "color": False,
    "legend": True,
    "version": False,
}
args_2 = {
    "infile": test_txt,
    "comments": None,
    "delimiter": None,
    "skip_header": 2,
    "skip_footer": 2,
    "usecols": (0, 1),
    "size": [60, 40],
    "x_limits": [0.0, 3.0],
    "y_limits": [0.0, 3.0],
    "scatter": True,
    "color": True,
    "legend": False,
    "version": True,
}
# Example with different delimiter
args_3 = {
    "infile": test_dat,
    "comments": None,
    "delimiter": "\t",
    "skip_header": 2,
    "skip_footer": 2,
    "usecols": (0, 1, 2, 3),
    "size": [40, 30],
    "x_limits": [0.0, 3.0],
    "y_limits": [0.0, 3.0],
    "scatter": False,
    "color": True,
    "legend": True,
    "version": True,
}
args_4 = {
    "infile": test_out,
    "comments": None,
    "delimiter": None,
    "skip_header": 0,
    "skip_footer": 0,
    "usecols": (0, 1),
    "size": [30, 20],
    "x_limits": None,
    "y_limits": None,
    "scatter": False,
    "color": False,
    "legend": True,
    "version": False,
}


def test_fnames():
    assert bashplot.get_args(opt={"infile": test_txt})["infile"] == test_txt


def test_options_scatter():
    assert bashplot.get_args(opt={"scatter": True})["scatter"] is True


def test_options_color():
    assert bashplot.get_args(opt={"color": True})["color"] is True


def test_options_legend():
    assert bashplot.get_args(opt={"legend": False})["legend"] is False


def test_options_version():
    assert bashplot.get_args(opt={"version": True})["version"] is True


def test_xlimits():
    assert bashplot.get_args(opt={"x_limits": [0.0, 20.0]})["x_limits"] == [0.0, 20.0]


def test_ylimits():
    assert bashplot.get_args(opt={"y_limits": [0.0, 20.0]})["y_limits"] == [0.0, 20.0]


def test_size():
    assert bashplot.get_args(opt={"size": [60, 60]})["size"] == [60, 60]


def test_ranges_default():
    assert bashplot.get_args()["size"] == [60, 40]


def test_usecols():
    assert bashplot.get_args(opt={"usecols": [0, 2, 5]})["usecols"] == [0, 2, 5]


@mock.patch("bashplot.bashplot.bashplot")
def test_default_run_mock(bashplot):
    bashplot.bashplot(fnames=test_txt, args=args_1)
    assert bashplot.bashplot.is_called


def test_default_run():
    bashplot.bashplot(fnames=test_txt, args=args_1)
    assert True


@mock.patch("bashplot.bashplot.bashplot")
def test_customize_run_mock_1(bashplot):
    bashplot.bashplot(fnames=test_txt, args=args_2)
    assert bashplot.bashplot.is_called


def test_customize_run_1():
    bashplot.bashplot(fnames=test_txt, args=args_2)
    assert True


@mock.patch("bashplot.bashplot.bashplot")
def test_customize_run_mock_2(bashplot):
    bashplot.bashplot(fnames=test_dat, args=args_3)
    assert bashplot.bashplot.is_called


def test_customize_run_2():
    bashplot.bashplot(fnames=test_dat, args=args_3)
    assert True


def test_customize_run_3():
    bashplot.bashplot(fnames=test_out, args=args_4)
    assert True


@mock.patch("bashplot.bashplot.command_line_runner")
def test_command_line_mock(command_line_runner):
    bashplot.command_line_runner()
    assert bashplot.command_line_runner.is_called


def test_command_line_1():
    bashplot.command_line_runner()
    assert True


def test_log(capfd):
    bashplot.log("msg")
    out, _ = capfd.readouterr()
    assert out == "msg\n"


def test_log_error(capfd):
    bashplot.log("msg", mode=True)
    out, _ = capfd.readouterr()
    assert out == "[ERROR] msg\n"
