from reo_toolkit import is_maori, ambiguous

def test_māori_word():
    assert is_maori('Ko matou ko nga Tino Rangatira o nga iwi o Nu Tireni', verbose = True)

def test_english_word():
    assert not is_maori('James Cook')
