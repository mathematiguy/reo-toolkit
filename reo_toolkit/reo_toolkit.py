import os
import re
import logging

from inflection import camelize
from functools import lru_cache

from .utils import is_camel_case, camel_case_split
from .wordlists import ambiguous, non_maori
from .encoders import Base
from .letters import vowels, consonants, numbers

double_consonants = re.compile('[{}][^{}]'.format(''.join(consonants), ''.join(vowels)))
non_maori_letters = re.compile("[ʻbcdfgjlqsvxyz]", re.IGNORECASE)
triple_vowels = re.compile('|'.join([r"{}{{3}}".format(ch) for ch in vowels]))
pacific_island = re.compile("[aeiouAEIOU]'[aeiouAEIOU]")
ends_with_consonant = re.compile('[{}]+'.format(
    ''.join(consonants) + ''.join(vowels)
))


def is_maori(text, strict = True, verbose = False):
    '''
    Returns True if the text provided matches Māori orthographical rules.

    `strict` - If True, `is_maori` returns False whenever an orthography rule is broken.
               If False, `is_maori` will use wordlists to reject common english words with
               māori language orthography

    `verbose` - (default False) If `True` display debugging messages

    There should be two modes of matching:
        - `Strong` means `is_maori` will return True only if it's certain the text is te reo māori.
        - `Weak` means `is_maori` will return True only if it can't prove that the text is not te reo māori.

    '''

    if verbose:
        logging.debug = print

    text = text.strip()

    splitter = re.compile(r'[\s\n\-]+')
    if splitter.search(text):
        # Split the text and evaluate each piece
        results = []
        for split in splitter.split(text):
            if len(split) == 0:
                logging.debug("Text {} gives an empty string when split".format(text))
                return False
            results.append(is_maori(split, strict = strict, verbose = verbose))
        return all(results)

    if is_camel_case(text):
        return all(is_maori(sub.lower(), strict = strict, verbose = verbose) \
                   for sub in camel_case_split(text))

    raw_text = text
    text = Base().encode(text)

    # Match letters found not in the māori alphabet
    non_maori_letters_result = non_maori_letters.search(text)
    if non_maori_letters_result:
        logging.debug("Letter '{}' not in maori character set".format(
                    non_maori_letters_result.group()))
        return False

    if len(text) == 0:
        if re.search('[A-z]', raw_text):
            # String is empty
            logging.debug("String {} is empty after cleaning".format(raw_text))
            return False
        else:
            return True

    if not strict:
        if text.lower() in non_maori:
            logging.debug("Text {} is in non_maori word list".format(text))
            return False

        if text.lower() in ambiguous:
            logging.debug("Text {} is in ambiguous word list".format(text))
            return False

    if len(text) == 1:
        if text in consonants:
            logging.debug("Single character word {} is a consonant".format(text))
            return False
        else:
            return True

    triple_vowels_result = triple_vowels.search(text)
    if triple_vowels_result:
        logging.debug("Text {} contains triple vowel '{}'".format(text, triple_vowels_result.group()))
        return False

    # Match consonants not followed by vowels
    double_consonants_result = double_consonants.search(text)
    if double_consonants_result:
        first, last = double_consonants_result.group()
        logging.debug("The consonant '{}' is followed by '{}' instead of a vowel in text '{}'".format(
            first, last, text))
        return False

    ends_with_consonant_result = ends_with_consonant.search(text)
    if ends_with_consonant_result:
        last_letter = ends_with_consonant_result.group()[-1]
        if last_letter in consonants:
            # Last character in word is a consonant
            logging.debug("The last character '{}' is a consonant: {}".format(
                    last_letter, text))
            return False

    pacific_island_result = pacific_island.search(text)
    if pacific_island_result:
        logging.debug('Contains a sequence {} that looks like it is from a Pacific Island language'.format(pacific_island_result.group()))
        return False


    return True
