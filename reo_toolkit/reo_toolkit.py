import os
import re
import logging

from inflection import camelize
from functools import lru_cache

from .utils import pairwise, is_camel_case, camel_case_split
from .wordlists import ambiguous, non_maori
from .encoders import BaseEncoder

vowels = set(r'AEIOUĀĒĪŌŪaeiouāēīōū')
consonants = set("HKMNPRTWŊƑhkmnprtwŋƒ")
numbers = set(map(str, range(10)))

_triple_vowels = re.compile('|'.join([r"{}{{3}}".format(ch) for ch in vowels]))

@lru_cache(maxsize=1024)
def is_maori(text, drop_ambiguous = False):
    '''
    Returns True if the text provided matches Māori orthographical rules.

    `drop_non_maori` - tell `is_maori` whether to ignore common english words that pass the
    orthography check based on a list of terms
    '''

    text = BaseEncoder().encode(text.lower())

    non_maori_chars = set(ch for ch in text if ch in 'bcdfgjlqsvxyz')
    if len(non_maori_chars) > 0:
        logging.debug("Text contains non-maori letters: {}".format(
            ', '.join(non_maori_chars)))
        return False

    if is_camel_case(text):
        return all(is_maori(sub.lower()) for sub in camel_case_split(text))


    # Remove non alphabet characters
    text = re.sub(r"[^{}0-9\-\s]".format(''.join(consonants.union(vowels))), "",
                  text).strip()

        return False

    if len(text) == 0:
        # String is empty
        logging.debug("String is empty after cleaning")

    if text in non_maori:
        logging.debug("Text {} is in non_maori word list".format(text))
        return False

    if drop_ambiguous and text in ambiguous:
        logging.debug("Text {} is in ambiguous word list".format(text))
        return False

    if len(text) == 1:
        if text in vowels:
            return True
        else:
            logging.debug("Single character word {} is not a vowel".format(text))
            return False

    if "-" in text:
        return all(is_maori(sub) for sub in text.split("-"))

    if _triple_vowels.search(text):
        return False

    for current_ch, next_ch in pairwise(text):
        if current_ch not in consonants.union(vowels).union(numbers).union(set(" ")):
            # Character not in maori character set
            logging.debug("Character '{}' not in maori character set".format(
                    current_ch))
            return False
        if current_ch in consonants:
            # The current character is a consonant, so the next must be a vowel
            if next_ch in vowels:
                # The next character is a vowel, so this is ok
                continue
            else:
                # The next character is not a vowel, this is not ok
                logging.debug("The consonant '{}' is followed by '{}' instead of a vowel: {}"\
                                  .format(current_ch, next_ch, text))
                return False

    if next_ch in consonants:
        # Last character in word is a consonant
        logging.debug("The last character '{}' is a consonant: {}".format(
                next_ch, text))
        return False

    if next_ch == "-" and not current_ch in vowels:
        logging.debug("The next character is {} but the current character {} is not a vowel"\
                  .format(next_ch, current_ch))
        return False

    return True
