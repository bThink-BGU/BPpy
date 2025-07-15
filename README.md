# BPpy: Behavioral Programming In Python
A Python implementation for the Behavioral Programming paradigm

## Installation
You can install ``bppy`` with pip:

```shell
pip install bppy
```

This does not include dependencies for gym integration. To install ``bppy`` with gym integration, use:

```shell
pip install bppy[gym]
```

If installation is not working, you can try upgrading pip:

```shell
pip install --upgrade pip
```

before submitting an issue.

In case you want to get started instantly and use ``bppy`` (with ``pynusmv`` and all dependencies) without installing it, you can use the [docker image](https://hub.docker.com/r/tomyaacov/bppy-docker):

```shell
docker run -it tomyaacov/bppy-docker
```


## Documentation
* [BPpy documentation](https://bppy.readthedocs.io/en/latest/)
* General introduction to Behavioral Programming can be found in [this](https://bpjs.readthedocs.io/en/develop/) BPjs tutorial and others

## Citing BPpy
To cite this repository in publications:
```
@inproceedings{yaacov_exploring_2025,
	title = {Exploring and Evaluating Interplays of BPpy with Deep Reinforcement Learning and Formal Methods},
	isbn = {978-989-758-742-9},
	doi = {10.5220/0013215200003928},
	booktitle = {Proceedings of the 20th International Conference on Evaluation of Novel Approaches to Software Engineering},
	publisher = {SciTePress},
	author = {Yaacov, Tom and Weiss, Gera and Ashrov, Adiel and Katz, Guy and Zisser, Jules},
	year = {2025},
	pages = {27--40},
}
```
