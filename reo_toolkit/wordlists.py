import os
from ahocorasick import Automaton

from .encoders import Base

def make_wordlist(filepath):
    with open(filepath, 'r') as f:
        wordlist = Automaton()
        for idx, word in enumerate(set(Base().encode(t) for t in f.read().split())):
            wordlist.add_word(word.lower(), (idx, word))
            wordlist.make_automaton()
    return wordlist

ambiguous = make_wordlist(os.path.join(os.path.dirname(__file__), 'ambiguous_terms.txt'))
non_maori = make_wordlist(os.path.join(os.path.dirname(__file__), 'non_maori_terms.txt'))
