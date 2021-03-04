from tqdm import tqdm
import pandas as pd
from reo_toolkit.encoders import *

def test_bilingual():
    assert Base().encode("Ko Murray tōku ingoa") == "Ko Murray tōku iŋoa"

def test_base_encode():
    assert Base().encode("Whiti mai te ra") == "Ƒiti mai te ra"

def test_base_decode():
    assert Base().decode("Ƒiti mai te ra") == "Whiti mai te ra"

def test_single_vowel_encode():
    assert SingleVowel().encode("Tēnā koe") == "Teenaa koe"

def test_single_vowel_decode():
    assert SingleVowel().decode("Teenaa koe") == "Tēnā koe"

def test_diphthong_encode():
    assert Diphthong().encode("Kua tae mai?") == "Kua tæ má?"

def test_diphthong_decode():
    assert Diphthong().decode("Kua tæ má?") == "Kua tae mai?"

def test_syllable_encode():
    assert Syllable().encode("Kei te pēhea koe?") == "케어 테 폐헤아 코에?"

def test_syllable_decode():
    assert Syllable().decode("케어 테 폐헤아 코에?") == "kei te pēhea koe?"

def test_double_vowel_encode():
    assert DoubleVowel().encode("whiti mai te ra") == "ƨƝƥƝ ƟƯ ƥƛ Ƥƚ"

def test_double_vowel_decode():
    assert DoubleVowel().decode("ƨƝƥƝ ƟƯ ƥƛ Ƥƚ") == "whiti mai te ra"

def test_long_syllable_encode():
    assert LongSyllable().encode("whiti mai te ra") == "ʁʄ Ȯ ʎ ʙ"

def test_long_syllable_decode():
    assert LongSyllable().decode("ʁʄ Ȯ ʎ ʙ") == "whiti mai te ra"
