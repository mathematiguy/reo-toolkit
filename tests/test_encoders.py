from reo_toolkit.encoders import NoEncoder, BaseEncoder, ShortmoraEncoder, MoraEncoder, SyllableEncoder

def test_no_encode():
    assert NoEncoder().encode("text") == "text"

def test_no_decode():
    assert NoEncoder().decode("text") == "text"

def test_base_encode():
    assert BaseEncoder().encode("whiti mai te ra") == "ƒiti mai te ra"

def test_base_decode():
    assert BaseEncoder().decode("ƒiti mai te ra") == "whiti mai te ra"

def test_shortmora_encode():
    assert ShortmoraEncoder().encode("Tēnā koe") == "Teenaa koe"

def test_shortmora_decode():
    assert ShortmoraEncoder().decode("Teenaa koe") == "Tēnā koe"

def test_mora_encode():
    assert MoraEncoder().encode("Kua tae mai") == "Kua tæ má"

def test_mora_decode():
    assert MoraEncoder().decode("Kua tæ má") == "Kua tae mai"

def test_syllable_encode():
    assert SyllableEncoder().encode("Kei te pēhea koe?") == "케어 테 폐헤아 코에?"

def test_syllable_decode():
    assert SyllableEncoder().decode("케어 테 폐헤아 코에?") == "kei te pēhea koe?"
