import setuptools
import os

def get_version(rel_path):
    with open(rel_path, "r") as fh:
        for line in fh:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "README.md"), "r") as fh:
    long_description = fh.read()

gym_dependencies = [
    "gymnasium>=0.28.1",
    "stable-baselines3>=2.0.0"
    ]
develop_dependencies = [
    "Sphinx>=5.3.0",
    "sphinx-rtd-theme>=1.2.1",
    "graphviz>=0.20.1",
    "pygame>=2.1.2"
]

setuptools.setup(
    name="bppy",
    version=get_version("bppy/__init__.py"),
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
        "z3-solver>=4.8.5.0"
    ],
    extras_require={
        "gym": gym_dependencies,
        "develop": gym_dependencies + develop_dependencies
    },
    python_requires='>=3.9'
)