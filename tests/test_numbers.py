from reo_toolkit.numbers import convert_numbers, digits_to_text


def test_digits_to_text():
    assert convert_numbers("10101") == "tekau mano rau mā tahi"


def test_convert_dollars():
    assert (
        convert_numbers("$12345") == "tekau mā rua mano toru rau whā tekau mā rima tāra"
    )


def test_convert_pounds():
    assert (
        convert_numbers("£54321")
        == "rima tekau mā whā mano toru rau rua tekau mā tahi pāuna"
    )
