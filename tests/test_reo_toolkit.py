from reo_toolkit import is_maori
from reo_toolkit.wordlists import non_maori

def test_māori_word():
    assert is_maori('Ko matou ko nga Tino Rangatira o nga iwi o Nu Tireni')

def test_english_word():
    assert not is_maori('James Cook')

def test_hyphen():
    assert not is_maori('-maori')

def test_long_hyphenated_word():
    assert is_maori('Taumatawhakatangi-hangakoauauotamatea-turipukakapikimaunga-horonukupokaiwhenua-kitanatahu')

def test_non_maori_word():
    assert not is_maori('tongue')

def test_triple_vowel():
    assert not is_maori("teee")

def test_camel_case():
    assert is_maori("KeiTePai")
    assert not is_maori("MeToo")

def test_te_tiriti_o_waitangi():
    with open('data/te-tiriti-o-waitangi.txt', 'r') as f:
        transcript = f.read()
        assert is_maori(transcript)

def test_he_whakaputanga():
    with open('data/he-whakaputanga.txt', 'r') as f:
        transcript = f.read()
        assert is_maori(transcript)
