import setuptools
import os
import bppy

VERSION = bppy.__version__

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bppy",
    version=VERSION,
    author="Tom Yaacov",
    author_email="tomyaacov1210@gmail.com",
    description="BPpy: Behavioral Programming In Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bThink-BGU/BPpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "z3-solver",
    ],
    #python_requires='>=3.6'
)