try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from pathlib import Path

import bashplot

__author__ = "Anselm Hahn"
__email__ = "Anselm.Hahn@gmail.com"


def long_description():
    #  deepcode ignore missing~close~open: <ignorable in the setup.py>
    readme = open(Path("./README.md")).read()
    changes = open(Path("./CHANGES.md")).read()
    todo = open(Path("./TODO.md")).read()

    long_description = (
        f"{readme}\n\n"
        "CHANGES\n"
        "-------\n"
        "{changes}\n"
        "TODO\n"
        "----\n"
        "{todo}\n"
    )
    return long_description


setup(
    name="bashplot",
    version=bashplot.__version__,
    description="Instant data plotting from the terminal into the terminal",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    install_requires=["numpy>=1.10", "plotille>=3.3",],
    packages=["bashplot",],
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    url="https://github.com/Anselmoo/bashplot",
    license='MIT',
    entry_points={
        "console_scripts": ["bashplot = bashplot.bashplot:command_line_runner"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Shells",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
)
