import os
import re

from .utils import pairwise
from functools import lru_cache

from .encoders import BaseEncoder

vowels = set(r'AEIOUĀĒĪŌŪaeiouāēīōū')
consonants = set("HKMNPRTWŊƑhkmnprtwŋƒ")
numbers = set(map(str, range(10)))


with open(os.path.join(os.path.dirname(__file__), 'ambiguous_terms.txt'), 'r') as f:
    ambiguous = set(f.read().split())


def is_maori(text, verbose=False):
@lru_cache(maxsize=1024)
    '''
    Returns True if the text provided matches Māori orthographical rules.

    If verbose == True, when the test fails the rules `is_maori` will tell you why it failed.
    '''

    text = BaseEncoder().encode(text.lower())

    non_maori_chars = set(ch for ch in text if ch in 'bcdfgjlqsvxyz')
    if len(non_maori_chars) > 0:
        if verbose:
            print("Text contains non-maori letters: {}".format(
                ', '.join(non_maori_chars)))
        return False

    # Remove non alphabet characters
    text = re.sub(r"[^{}0-9\-\s]".format(''.join(consonants.union(vowels))), "",
                  text).strip()

    if len(text) == 0:
        # String is empty
        if verbose: print("String is empty after cleaning")
        return False
    if len(text) == 1:
        if text in vowels:
            return True
        else:
            if verbose:
                print("Single character word {} is not a vowel".format(text))
            return False

    if text[0] == "-":
        if verbose:
            "Starts with hyphen and no preceding letter"
        return False

    for current_ch, next_ch in pairwise(text):
        if current_ch not in consonants.union(vowels).union(numbers).union(set(" ")):
            # Character not in maori character set
            if verbose:
                print("Character '{}' not in maori character set".format(
                    current_ch))
            return False
        if current_ch in consonants:
            # The current character is a consonant, so the next must be a vowel
            if next_ch in vowels:
                # The next character is a vowel, so this is ok
                continue
            else:
                # The next character is not a vowel, this is not ok
                if verbose:
                    print("The consonant '{}' is followed by '{}' instead of a vowel: {}"\
                                  .format(current_ch, next_ch, text))
                return False
    if next_ch in consonants:
        # Last character in word is a consonant
        if verbose:
            print("The last character '{}' is a consonant: {}".format(
                next_ch, text))
        return False
    if next_ch == "-" and not current_ch in vowels:
        if verbose:
            print("The next character is {} but the current character {} is not a vowel"\
                  .format(next_ch, current_ch))
        return False
    return True

