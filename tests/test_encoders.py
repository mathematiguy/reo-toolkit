from tqdm import tqdm
import pandas as pd
from reo_toolkit.encoders import *

def test_base_encode():
    assert Base().encode("Whiti mai te ra") == "Ƒiti mai te ra"

def test_base_decode():
    assert Base().decode("Ƒiti mai te ra") == "Whiti mai te ra"

def test_single_vowel_encode():
    assert SingleVowel().encode("Tēnā koe") == "Teenaa koe"

def test_single_vowel_decode():
    assert SingleVowel().decode("Teenaa koe") == "Tēnā koe"

def test_mora_encode():
    assert Mora().encode("Kua tae mai") == "Kua tæ má"

def test_mora_decode():
    assert Mora().decode("Kua tæ má") == "Kua tae mai"

def test_syllable_encode():
    assert Syllable().encode("Kei te pēhea koe?") == "케어 테 폐헤아 코에?"

def test_syllable_decode():
    assert Syllable().decode("케어 테 폐헤아 코에?") == "kei te pēhea koe?"
