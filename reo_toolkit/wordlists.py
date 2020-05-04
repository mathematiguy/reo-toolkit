import os

from .encoders import BaseEncoder

with open(os.path.join(os.path.dirname(__file__), 'ambiguous_terms.txt'), 'r') as f:
    ambiguous = set(BaseEncoder().encode(t) for t in f.read().split())

with open(os.path.join(os.path.dirname(__file__), 'non_maori_terms.txt'), 'r') as f:
    non_maori = set(BaseEncoder().encode(t) for t in f.read().split())
