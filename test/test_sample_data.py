import os
import unittest

import numpy as np


def generate(fname="test_data.txt"):
    """Generation of example test-set.

    generate() generates an example test-set for sin from -2 * pi to +2 * pi for sinus.
    

    Parameters
    ----------
    fname : str, optional
        Filename of the to exported ASCII-data. Default is `test_data.txt`.
    """

    x = np.linspace(-2 * np.pi, 2 * np.pi)
    y = np.sin(x)

    data = np.array([x, y]).T
    np.savetxt(fname, data)


if __name__ == "__main__":
    generate()
