.. BPpy documentation master file, created by
   sphinx-quickstart on Wed May 31 15:43:12 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BPpy's documentation!
================================

BPpy is a Python implementation for the Behavioral Programming paradigm.

A general introduction to Behavioral Programming can be found in `this <https://bpjs.readthedocs.io/en/develop>`_ BPjs tutorial and others.

+++++++++++++++
Installation
+++++++++++++++
You can install ``bppy`` with pip:

.. code-block:: shell

   pip install bppy

This does not include dependencies for gym integration. To install ``bppy`` with gym integration, use:

.. code-block:: shell

   pip install bppy[gym]

If installation is not working, you can try upgrading pip:

.. code-block:: shell

   pip install --upgrade pip

before submitting an issue.

In case you want to get started instantly and use ``bppy`` (with ``pynusmv`` and all dependencies) without installing it, you can use the `docker image <https://hub.docker.com/r/tomyaacov/bppy-docker>`_:

.. code-block:: shell

   docker run -it tomyaacov/bppy-docker


.. toctree::
   :maxdepth: 2
   :caption: Contents

   modules
   Examples/examples



+++++++++++++++
Citing BPpy
+++++++++++++++
To cite this repository in publications:

.. code-block:: none

   @misc{bppy,
         author = {Tom Yaacov},
         title = {BPpy: Behavioral Programming In Python},
         year = {2020},
         publisher = {GitHub},
         journal = {GitHub repository},
         howpublished = {\url{https://github.com/bThink-BGU/BPpy}},
         }

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
