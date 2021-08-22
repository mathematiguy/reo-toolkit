FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Use New Zealand mirrors
RUN sed -i 's/archive/nz.archive/' /etc/apt/sources.list

# Install python + other things
RUN apt update
RUN apt install -y python3-dev python3-pip

COPY . /code
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

# Need this for the nltk.tokenizers package
ENV NLTK_DATA /nltk_data
RUN python3 -c "import nltk;nltk.download('punkt', download_dir='$NLTK_DATA')"
