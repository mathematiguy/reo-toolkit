import re


def convert_numbers(text):
    text = prepare_numbers(text)
    while re.search('[0-9]*,?[0-9]{1,3}', text):
        start, finish = re.search('[0-9]*,?[0-9]{1,3}', text).span()
        text = text[:start] + digits_to_text(
            int(text[start:finish].replace(",", ""))) + text[finish:]
    return text


def prepare_numbers(text):
    '''
    This function removes dollar ($) and pound (£) symbols
    and also percent (%) symbols, replacing the text with the
    correct māori usage for each term.
    '''
    while True:
        if "£" in text:
            start, finish = re.search("£[0-9]+", text).span()
            text = text[:start] + text[start +1:finish] + \
                str.rstrip(" pāuna " + text[finish +1:])
        elif "$" in text:
            start, finish = re.search(r"\$[0-9]+", text).span()
            text = text[:start] + text[start +1:finish] + \
                   str.rstrip(" tāra " + text[finish + 1:])
        elif re.search(r"[0-9]\-[0-9]", text):
            start, finish = re.search(r"[0-9]\-[0-9]", text).span()
            text = text[:start + 1] + ' ki te ' + text[finish - 1:]
        elif re.search("[0-9]%", text):
            start, finish = re.search("[0-9]%", text).span()
            text = text[:start + 1] + ' paihēneti' + text[finish:]
        else:
            break
    return text


def digits_to_text(num, warn=True):

    if warn and abs(num) >= 1000000:
        warnings.warn("Only numbers below 1,000,000 can be translated")
        return str(num)

    digits = [int(i) for i in str(num)]

    ones = [
        'kore', 'tahi', 'rua', 'toru', 'whā', 'rima',
        'ono', 'whitu', 'waru', 'iwa'
    ]
    places = ['rau', 'tekau', 'mano', 'rau', 'tekau', '']

    ones_dict = dict(zip([i for i in range(10)], ones))
    places_dict = dict(zip([5, 4, 3, 2, 1, 0], places))

    digit_words = []
    for place, digit in enumerate(digits[::-1]):
        ones_digit = ones_dict[digit]

        place_digit = places_dict[place]

        if ones_digit == "kore" and num != 0:
            if place_digit == "mano":
                digit_words += ["mano"]
            continue

        if place_digit in ['rau', 'mano'] and ones_digit == 'tahi':
            ones_digit = "kotahi"
        elif place in [0, 3]:
            ones_digit = "mā " + ones_digit

        place_words = str.strip(ones_digit + " " + place_digit)

        digit_words.append(place_words)

    digit_text = ' '.join(digit_words[::-1])

    digit_text = re.sub("tahi tekau", "tekau", digit_text)
    digit_text = re.sub("mano kotahi", "mano", digit_text)
    digit_text = re.sub("mā kotahi", "mā tahi", digit_text)
    digit_text = re.sub("^mā", "", digit_text)
    digit_text = re.sub(r"\s{2,}", " ", digit_text)

    return digit_text.strip()
