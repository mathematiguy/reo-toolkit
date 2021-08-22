#! /bin/bash
set -ex

# Install package
pip3 install -e .

# Install nltk tokenizers
python3 -c "import nltk;nltk.download('punkt', download_dir='/nltk_data')"

# Run tests
make test
