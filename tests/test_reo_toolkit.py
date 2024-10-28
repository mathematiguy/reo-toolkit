from reo_toolkit import is_maori
from reo_toolkit.wordlists import non_maori


def test_māori_word():
    assert is_maori("Ko matou ko nga Tino Rangatira o nga iwi o Nu Tireni")


def test_macron():
    assert is_maori("tohutō")


def test_macron_combining_character():
    """The unicode code point \u0304 is a combining character that adds a macron to the preceding letter"""
    assert is_maori("a\u0304".encode("utf-8").decode())


def test_english_word():
    assert not is_maori("James Cooks")


def test_double_consonant():
    assert not is_maori("mmea")


def test_ending_consonant():
    assert not is_maori("new")


def test_non_maori_letter():
    assert not is_maori("z")


def test_ambiguous_word():
    assert not is_maori("a", strict=False)
    assert is_maori("a", strict=True)


def test_cleaning():
    # This non-maori word gives a maori word 'i' after the non-maori characters are removed
    assert not is_maori("six")


def test_hyphen():
    assert not is_maori("-maori")


def test_long_hyphenated_word():
    assert is_maori(
        "Taumatawhakatangi-hangakoauauotamatea-turipukakapikimaunga-horonukupokaiwhenua-kitanatahu"
    )


def test_ng():
    assert is_maori("ranginui")


def test_non_maori_word():
    assert not is_maori("tongue", strict=False)


def test_triple_vowel():
    assert not is_maori("teee")


def test_many_vowels():
    assert is_maori("Papaoiea")


def test_camel_case():
    assert is_maori("KeiTePai")
    assert not is_maori("MeToo", strict=False)


def test_apostrophe():
    assert is_maori(
        "Ko 'Mā whero, mā pango, ka oti te mahi' ētahi o ngā whakatauki rongonui"
    )


def test_pacific_island():
    assert not is_maori("ma'unga")


def test_okina():
    assert not is_maori(" ʻokina")


def test_all_caps():
    assert is_maori("WHĀTUA")


def test_alphanum():
    assert not is_maori("i18n")


def test_number():
    assert is_maori("2009")


def test_te_tiriti_o_waitangi():
    with open("data/te-tiriti-o-waitangi.txt", "r") as f:
        transcript = f.read()
        assert is_maori(transcript, strict=True)


def test_he_whakaputanga():
    with open("data/he-whakaputanga.txt", "r") as f:
        transcript = f.read()
        assert is_maori(transcript, strict=True)


def test_sentence():
    assert is_maori(
        "inā tatū te tai ka puare tēnei toka ka taea te haere mai i reira ki uta",
        strict=True,
    )
