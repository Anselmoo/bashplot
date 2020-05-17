#!/usr/bin/env python

"""Test for basplot."""
from glob import glob
from pathlib import Path
import unittest

from bashplot import bashplot


class BashplotTestCase(unittest.TestCase):
    def call_bashplot(self, args):
        args = bashplot.get_args()
        return bashplot.bashplot(args)

    def setUp(self):
        self.infile = glob("test*.txt")
        self.args_1 = {
            "infile": self.infile,
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
        self.args_2 = {
            "infile": self.infile,
            "comments": None,
            "delimiter": None,
            "skip_header": 2,
            "skip_footer": 2,
            "usecols": (0, 1),
            "size": [60,40],
            "x_limits": [0.0, 3.0],
            "y_limits": [0.0, 3.0],
            "scatter": True,
            "color": True,
            "legend": False,
            "version": True,
        }
        # Example with different delimiter
        self.singlefile = [Path("./test_data_mixed.dat")]
        self.args_3 = {
            "infile": self.singlefile,
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

    def test_fnames(self):
        self.assertEqual(
            bashplot.get_args(opt={"infile": self.infile})["infile"], self.infile
        )

    def test_options(self):
        self.assertTrue(bashplot.get_args(opt={"scatter": True})["scatter"])
        self.assertTrue(bashplot.get_args(opt={"color": True})["color"])
        self.assertFalse(bashplot.get_args(opt={"legend": False})["legend"])
        self.assertTrue(bashplot.get_args(opt={"version": True})["version"])

    def test_ranges(self):
        self.assertEqual(
            bashplot.get_args(opt={"x_limits": [0.0, 20.0]})["x_limits"], [0.0, 20.0]
        )
        self.assertEqual(
            bashplot.get_args(opt={"y_limits": [0.0, 20.0]})["y_limits"], [0.0, 20.0]
        )
        self.assertEqual(bashplot.get_args(opt={"size": [60, 60]})["size"], [60, 60])
        self.assertEqual(bashplot.get_args()["size"], [60, 40])
        self.assertEqual(
            bashplot.get_args(opt={"usecols": [0, 2, 5]})["usecols"], [0, 2, 5]
        )

    def test_default_run(self):
        bashplot.bashplot(fnames=self.infile, args=self.args_1)
        assert 1

    def test_customize_run_1(self):
        bashplot.bashplot(fnames=self.infile, args=self.args_2)
        assert 1

    def test_customize_run_2(self):
        bashplot.bashplot(fnames=self.singlefile, args=self.args_3)
        assert 1


if __name__ == "__main__":
    unittest.main()
