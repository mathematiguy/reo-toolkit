from reo_toolkit.numbers import convert_numbers, digits_to_text

def test_digits_to_text():
    assert convert_numbers('12345') == 'tekau mā rua mano toru rau whā tekau mā rima'

def test_convert_numbers():
    assert convert_numbers('$12345') == 'tekau mā rua mano toru rau whā tekau mā rima tāra'
