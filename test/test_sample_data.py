from pathlib import Path
import numpy as np


def generate(fname="test_data"):
    """Generation of example test-sets.

    generate() generates an example test-sets for:
    1.  sin from -2 * pi to +2 * pi for sinus.
    2.  cos from -2 * pi to +2 * pi for cosinus.
    3.  random gaussian distribution 

    Parameters
    ----------
    fname : str, optional
        Filename of the to exported ASCII-data. Default is `test_data.txt`.
    """

    x = np.linspace(-2 * np.pi, 2 * np.pi)

    y_1 = np.sin(x)
    data = np.array([x, y_1]).T
    np.savetxt(Path(f"./{fname}_sin.txt"), data)

    y_2 = np.cos(x)
    data = np.array([x, y_2]).T
    np.savetxt(Path(f"./{fname}_cos.txt"), data)
    
    data = np.array([x, y_1, y_2]).T
    np.savetxt(Path(f"./{fname}_mixed.txt"), data)
    
    mu, sigma = 0, 0.1  # mean and standard deviation
    x = np.linspace(-0.3, 0.3)
    y = np.random.normal(mu, sigma, 50)
    data = np.array([x, y]).T
    np.savetxt(Path(f"./{fname}_gaussian.txt"), data)


if __name__ == "__main__":
    generate()
