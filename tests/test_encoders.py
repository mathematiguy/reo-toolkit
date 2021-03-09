from reo_toolkit.encoders import *

bilingual_sent = "ko murray tōku ingoa"

def test_encoder():
    base = get_encoder('base')
    assert base.encode('kupu') == 'kupu'

def test_bilingual_base():
    assert Base().decode(Base().encode(bilingual_sent)) == bilingual_sent

def test_bilingual_diphthong():
    assert Diphthong().decode(Diphthong().encode(bilingual_sent)) == bilingual_sent

def test_bilingual_singlevowel():
    assert SingleVowel().decode(SingleVowel().encode(bilingual_sent)) == bilingual_sent

def test_bilingual_doublevowel():
    assert DoubleVowel().decode(DoubleVowel().encode(bilingual_sent)) == bilingual_sent

def test_bilingual_syllable():
    bilingual_sent = 'ko te rata te next one'
    assert Syllable().decode(Syllable().encode(bilingual_sent)) == bilingual_sent

def test_bilingual_longsyllable():
    assert LongSyllable().decode(LongSyllable().encode(bilingual_sent)) == bilingual_sent

def test_all_caps():
    assert Base().decode(Base().encode('NGĀ MŌTEATEA')) == "NGĀ MŌTEATEA"

def test_comma():
    assert Syllable().decode(Syllable().encode('39 tiriti o pipitea,')) == '39 tiriti o pipitea,'

def test_quotation_mark():
    assert Syllable().decode(Syllable().encode("‘kua whānau. aue!’")) == "‘kua whānau. aue!’"

def test_base_encode():
    assert Base().encode("Whiti mai te ra") == "Ƒiti mai te ra"

def test_base_decode():
    assert Base().decode("Ƒiti mai te ra") == "Whiti mai te ra"

def test_single_vowel_encode():
    assert SingleVowel().encode("Tēnā koe") == "Teenaa koe"

def test_single_vowel_decode():
    assert SingleVowel().decode("Teenaa koe") == "Tēnā koe"

def test_diphthong_encode():
    assert Diphthong().encode("Kua tae mai ngā iwi?") == "Kua tæ má ŋā iwi?"

def test_diphthong_decode():
    assert Diphthong().decode("Kua tæ má ngā iwi?") == "Kua tae mai ngā iwi?"

def test_syllable_encode():
    assert Syllable().encode("Kei te pēhea koe?") == "케어 테 폐헤아 코에?"

def test_syllable_decode():
    assert Syllable().decode("케어 테 폐헤아 코에?") == "kei te pēhea koe?"

def test_syllable_alphanum():
    sent = 'i18n me l10n i roto i te reo ipurangi'
    assert Syllable().decode(Syllable().encode(sent)) == sent

def test_double_vowel_encode():
    assert DoubleVowel().encode("whiti mai te ra") == "ƨƝƥƝ ƟƯ ƥƛ Ƥƚ"

def test_double_vowel_decode():
    assert DoubleVowel().decode("ƨƝƥƝ ƟƯ ƥƛ Ƥƚ") == "whiti mai te ra"

def test_long_syllable_encode():
    assert LongSyllable().encode("whiti mai te ra") == "ʁʄ Ȯ ʎ ʙ"

def test_long_syllable_decode():
    assert LongSyllable().decode("ʁʄ Ȯ ʎ ʙ") == "whiti mai te ra"
