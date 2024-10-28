"""
An alphabet derived from pairs of consonant+(vowel|long vowel|diphthong).
Diphthong is as defined by te reo Māori speakers.

A sample is provided to encode text to this alphabet. We take a hungry
approach where the longest string is prioritised. Sometimes prefixes
break this rule so we provide a mechanism to handle them as an edge
case.

This alphabet was inspired by the way we learnt soungs growing up. When
reading the polynesian alphabet, it's common to read the consonants as
"he, ke, la, mu, pu, nu, we,". When practicing diphthongs, it oftens
helps to practice them in context e.g. wai, kou, kau, tae.
"""

from unidecode import unidecode
import re
from random import random

CONSONANTS = ["h", "k", "m", "n", "p", "r", "t", "w", "ƒ", "ŋ"]
VOWELS = ["a", "e", "i", "o", "u"]
LONG_VOWELS = ["ā", "ē", "ī", "ō", "ū"]
DIPHTHONGS = [
    "ae",
    "ai",
    "ao",
    "au",
    "ei",
    "oi",
    "oe",
    "ou",
    "āe",
    "āi",
    "āo",
    "āu",
    "ēi",
    "ōi",
    "ōe",
    "ōu",
]

PREFIXES = [("ƒaka", "∑", ["ƒa", "ka"])]


def is_prefix(char):
    for i, j, k in PREFIXES:
        if char == j:
            return True
    return False


def get_syll_for_prefix(prefix):
    for i, j, k in PREFIXES:
        if prefix == j:
            return k


def alphabet6():
    for mea in DIPHTHONGS + LONG_VOWELS + VOWELS:
        for consonant in CONSONANTS + [" "]:
            s = (consonant + mea).strip()
            yield s


def normalise(text):
    return (
        text.replace("wh", "ƒ")
        .replace("ng", "ŋ")
        .replace("  ", " ")
        .replace("ƒaka", "∑")
    )


def denormalise(text):
    return text.replace("ƒ", "wh").replace("ŋ", "ng").replace("∑", "ƒaka")


def test_encode_to_syllables():

    with open(
        "/Volumes/GoogleDrive-102052350554870542074/Shared drives/Backup/Kōrero Māori Data/From Te Taka/Hiku/Google Maori Copora/KupuMI01.txt",
        "r",
        encoding="utf8",
    ) as f:
        line = f.readline()
        while line:
            phrase = normalise(line.strip().lower())

            matches = []
            munch = ""
            chars = ""
            syllable = []
            for char in phrase:
                munch += char
                if munch in CONSONANTS:
                    continue
                if munch in alphabet6():
                    matches.append(munch)
                else:
                    if len(matches) > 0:
                        syllable.append(matches[-1])
                    elif len(matches) == 1:
                        syllable.append(matches[0])
                    if char in ["-", " "]:
                        syllable.append(char)
                        munch = ""
                        matches = []
                    elif is_prefix(char):
                        syllable += get_syll_for_prefix(char)
                        munch = ""
                        matches = []
                    else:
                        munch = munch[-1]
                        matches = [munch]
            if matches:
                syllable.append(matches[-1])
            else:
                syllable.append(munch)

            phrase_syllable = "+".join(syllable).replace("+ +", " ").replace("+-+", "-")

            if random() < 0.0005 or "∑utu" in phrase or "aa" in phrase:
                print(f"{denormalise(phrase)} || {denormalise(phrase_syllable)}")

            a = unidecode(phrase.replace("∑", "ƒaka"))
            b = unidecode(phrase_syllable).replace("+", "")
            if a != b:
                print(phrase)
                raise ValueError(f"{a} != {b}")

            line = f.readline()
