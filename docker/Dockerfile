# Use Ubuntu 22.04 as base
FROM ubuntu:22.04

# Set environment variables to ensure non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && apt-get install -y \
    swig \
    flex \
    bison \
    patchelf \
    software-properties-common \
    curl \
 && add-apt-repository ppa:deadsnakes/ppa \
 && apt-get update \
 && apt-get install -y python3.9 python3.9-venv python3.9-dev \
 && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
 && python3.9 get-pip.py

RUN python3.9 -m venv /venv
ENV PATH=/venv/bin:$PATH

# Install the required Python packages
RUN python3 -m pip install \
    bppy==0.0.8 \
    z3-solver>=4.8.5.0 \
    gymnasium==0.28.1 \
    stable-baselines3==2.0.0 \
    https://github.com/davidebreso/pynusmv/releases/download/v1.0rc8/pynusmv-1.0rc8-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    Sphinx>=5.3.0 \
    sphinx-rtd-theme>=1.2.1 \
    graphviz>=0.20.1


# Cleanup to reduce image size
RUN apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && rm get-pip.py

# Define a default command, for this case, we're just using a bash shell
CMD ["/bin/bash"]
