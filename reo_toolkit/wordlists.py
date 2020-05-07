import os
from ahocorasick import Automaton

from .encoders import BaseEncoder

def make_wordlist(filepath):
    with open(filepath, 'r') as f:
        wordlist = Automaton()
        for idx, word in enumerate(set(BaseEncoder().encode(t) for t in f.read().split())):
            wordlist.add_word(word, (idx, word))
            wordlist.make_automaton()
    return wordlist

ambiguous = make_wordlist(os.path.join(os.path.dirname(__file__), 'ambiguous_terms.txt'))
non_maori = make_wordlist(os.path.join(os.path.dirname(__file__), 'non_maori_terms.txt'))
