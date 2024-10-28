import os
import re
import logging

from inflection import camelize
from functools import lru_cache

from .utils import is_camel_case, camel_case_split
from .wordlists import ambiguous, non_maori
from .encoders import Base
from .letters import vowels, consonants, alphabet, numbers

double_consonants = re.compile("[{}][^{}]".format("".join(consonants), "".join(vowels)))
non_maori_letters = re.compile("[ʻbcdfgjlqsvxyz]", re.IGNORECASE)
triple_vowels = re.compile("|".join([r"{}{{3}}".format(ch) for ch in vowels]))
pacific_island = re.compile("[aeiouAEIOU]'[aeiouAEIOU]")
alphanum = re.compile("[{}]+[0-9]+".format("".join(alphabet)))
ends_with_consonant = re.compile("[{}]+".format("".join(consonants) + "".join(vowels)))


def is_maori(text, strict=True, verbose=False):
    """
    Determine if a given text is in Māori language.

    This function evaluates whether a provided string adheres to the rules of the Māori language.
    It performs checks for non-Māori characters, specific language patterns, and ensures that
    the text conforms to Māori phonotactics.

    Parameters:
    text (str): The text to be evaluated.
    strict (bool): If True, enforces stricter checks against a predefined non-Māori word list and ambiguous words. Defaults to True.
    verbose (bool): If True, enables detailed debug output to the console. Defaults to False.

    Returns:
    bool: True if the text is determined to be Māori, False otherwise.

    Notes:
    - The function handles camelCase text by splitting and evaluating each component separately.
    - It uses regular expressions to identify and remove non-alphabetic characters, and to match
      specific Māori language patterns.
    - It considers various edge cases such as empty strings after cleaning, single-character words,
      triple vowels, double consonants, and words ending with consonants.
    - When `strict` is set to False, the function allows for some leniency in recognizing words
      that might be Māori.

    Examples:
    >>> is_maori("kia ora")
    True
    >>> is_maori("hello")
    False
    >>> is_maori("KiaOra", strict=False)
    True
    >>> is_maori("whakawhetai", verbose=True)
    True
    """

    if verbose:
        logging.debug = print

    text = text.strip()

    splitter = re.compile(r"[\s\n\-]+")
    if splitter.search(text):
        # Split the text and evaluate each piece
        results = []
        for split in splitter.split(text):
            if len(split) == 0:
                logging.debug("Text {} gives an empty string when split".format(text))
                return False
            results.append(is_maori(split, strict=strict, verbose=verbose))
        return all(results)

    if is_camel_case(text):
        return all(
            is_maori(sub.lower(), strict=strict, verbose=verbose)
            for sub in camel_case_split(text)
        )

    raw_text = text
    text = Base().encode(text)

    # Match letters found not in the māori alphabet
    non_maori_letters_result = non_maori_letters.search(text)
    if non_maori_letters_result:
        logging.debug(
            "Letter '{}' not in maori character set".format(
                non_maori_letters_result.group()
            )
        )
        return False

    if len(text) == 0:
        if re.search("[A-z]", raw_text):
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
        logging.debug(
            "Text {} contains triple vowel '{}'".format(
                text, triple_vowels_result.group()
            )
        )
        return False

    # Match consonants not followed by vowels
    double_consonants_result = double_consonants.search(text)
    if double_consonants_result:
        first, last = double_consonants_result.group()
        logging.debug(
            "The consonant '{}' is followed by '{}' instead of a vowel in text '{}'".format(
                first, last, text
            )
        )
        return False

    ends_with_consonant_result = ends_with_consonant.search(text)
    if ends_with_consonant_result:
        last_letter = ends_with_consonant_result.group()[-1]
        if last_letter in consonants:
            # Last character in word is a consonant
            logging.debug(
                "The last character '{}' is a consonant: {}".format(last_letter, text)
            )
            return False

    pacific_island_result = pacific_island.search(text)
    if pacific_island_result:
        logging.debug(
            "Contains a sequence {} that looks like it is from a Pacific Island language".format(
                pacific_island_result.group()
            )
        )
        return False

    alphanum_result = alphanum.search(text)
    if alphanum_result:
        logging.debug(
            "Contains numbers and letters together: {}".format(alphanum_result.group())
        )
        return False

    return True
