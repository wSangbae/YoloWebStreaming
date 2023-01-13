FROM ubuntu:18.04
MAINTAINER Wimes <w.sangbae@hdc-labs.com>

# Update the package manager and install wget
RUN apt-get update && apt-get install -y wget

# Download the Anaconda installer
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2021.07-Linux-x86_64.sh -O anaconda.sh

# Run the Anaconda installer
RUN /bin/bash anaconda.sh -b -p /opt/anaconda3

# Add Anaconda to the PATH
ENV PATH /opt/anaconda3/bin:$PATH

# Update conda and install some packages
RUN conda update -n base -c defaults conda && \
    conda install -y pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch \
    pip install opencv-python==4.5.5.64
    conda install -y numpy pandas matplotlib scikit-learn flask pyyaml tqdm seaborn scipy\
