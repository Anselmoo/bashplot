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
    #  deepcode ignore missing~close~open: <ignorable in the setup.py>
    changes = open(Path("./CHANGES.md")).read()
    #  deepcode ignore missing~close~open: <ignorable in the setup.py>
    todo = open(Path("./TODO.md")).read()

    long_description = (
        f"{readme}\n\n"
        f"CHANGES\n"
        f"-------\n"
        f"{changes}\n"
        f"TODO\n"
        f"----\n"
        f"{todo}\n"
    )
    return long_description


def requirments():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="bashplot",
    version=bashplot.__version__,
    description="Instant data plotting from the terminal into the terminal",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    install_requires=requirments(),
    packages=[
        "bashplot",
    ],
    py_modules=[path.stem for path in Path(".").glob("bashplot/*.py")],
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    url="https://github.com/Anselmoo/bashplot",
    license="MIT",
    entry_points={
        "console_scripts": ["bashplot = bashplot.bashplot:command_line_runner"]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Shells",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    keywords=[
        "terminal",
        "data-visualization",
        "data-science",
        "database",
    ],
    extras_require={"testing": ["pipenv"]},
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    test_suite='pytest',
)
