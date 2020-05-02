import re

from .utils import pairwise
from .encoders import BaseEncoder

vowels = list('aeiouāēīōū')
consonants = list("hkmnprtwŋƒ")
numbers = list(map(str, range(10)))


def is_maori(text, verbose=False):
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
    text = re.sub(r"[^{}0-9\s]".format(''.join(consonants + vowels)), "",
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
    for current_ch, next_ch in pairwise(text):
        if current_ch not in consonants + vowels + numbers + [" "]:
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
    return True

