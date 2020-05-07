FROM dragonflyscience/dragonverse-18.04:latest

# Install python + other things
RUN apt update
RUN apt install -y python3-dev python3-pip

# Install jupyterlab
RUN pip3 install jupyter jupyterlab ipython pandas numpy matplotlib jsonlines pytest-xdist pytest-benchmark


COPY . /code
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

# Need this for the nltk.tokenizers package
RUN python3 -m nltk.downloader punkt

RUN Rscript -e 'install.packages("here")'
RUN Rscript -e 'install.packages("furrr")'

