import re
import nltk
import jamo
import logging

_vowels = set(r'AEIOUĀĒĪŌŪaeiouāēīōū')
_consonants = set("HKMNPRTWŊƑhkmnprtwŋƒ")
_numbers = set(map(str, range(10)))


class Base:

    encoder_dict = {
        'N[Gg]': 'Ŋ',
        'W[Hh]': 'Ƒ',
        'ng': 'ŋ',
        'wh': 'ƒ'
    }

    decoder_dict = {
        'Ŋ': 'Ng',
        'Ƒ': 'Wh',
        'ŋ': 'ng',
        'ƒ': 'wh'
    }

    def encode(self, text):
        for k, v in self.encoder_dict.items():
            text = re.sub(k, v, text)
        return text

    def decode(self, text):
        for k, v in self.decoder_dict.items():
            text = re.sub(k, v, text)
        return text



class SingleVowel:

    encoder_dict = {
        'ā': 'aa',
        'ē': 'ee',
        'ī': 'ii',
        'ō': 'oo',
        'ū': 'uu',
        'ng': 'ŋ',
        'wh': 'ƒ'
    }

    decoder_dict = {v:k for k,v in encoder_dict.items()}

    def encode(self, text):
        for k, v in self.encoder_dict.items():
            text = text.replace(k, v)
        return text

    def decode(self, text):

        for k, v in self.decoder_dict.items():
            if k in text:
                text = text.replace(k, v)

        return text


class Diphthong:

    encoder_dict = {
        'ae': 'æ',
        'ai': 'á',
        'ao': 'å',
        'au': 'ä',
        'ei': 'é',
        'oe': 'œ',
        'oi': 'ó',
        'ou': 'ö',
        'ng': 'ŋ',
        'wh': 'ƒ',
    }

    decoder_dict = {v: k for k, v in encoder_dict.items()}

    def tokenize(self, text, keep_spaces = False):
        while len(text) > 0:
            if keep_spaces and text[0] in [" ", "-"]:
                yield text[0]
                text = text[1:]
            if text[0] in _consonants:
                yield text[0]
                text = text[1:]
            elif text[0] in _vowels:
                if len(text) > 1 and text[1] in _vowels:
                    if text[:2] in self.encoder_dict.keys():
                        yield text[:2]
                        text = text[2:]
                    else:
                        yield text[0]
                        text = text[1:]
                else:
                    yield text[0]
                    text = text[1:]
            else:
                text = text[1:]
                continue

    def encode(self, text):
        encoded_sents = []
        for sent in text.split("\n"):
            sent_encoded = []
            for mora in self.tokenize(sent, keep_spaces = True):
                if mora in [" ", "-"]:
                    sent_encoded.append(mora)
                    continue
                try:
                    if len(mora) > 1 or mora == "f":
                        sent_encoded.append(self.encoder_dict[mora])
                        continue
                except KeyError:
                    logging.error("KeyError: mora {} not in encoder_dict".format(mora))
                sent_encoded.append(mora)
            text_encoded = ''.join(sent_encoded)
            encoded_sents.append(text_encoded)
        return '\n'.join(encoded_sents)

    def decode(self, encoded_text):
        for diphthong, mora in self.encoder_dict.items():
             encoded_text = encoded_text.replace(mora, diphthong)
        return encoded_text


class Syllable:

    encoder_dict = {
        'a': 'ᅡ',
        'ā': 'ᅣ',
        'ē': 'ᅨ',
        'e': 'ᅦ',
        'i': 'ᅥ',
        'ī': 'ᅧ',
        'o': 'ᅩ',
        'ō': 'ᅭ',
        'u': 'ᅮ',
        'ū': 'ᅲ',
        'h': 'ᄒ',
        'k': 'ᄏ',
        'm': 'ᄆ',
        'n': 'ᄂ',
        'p': 'ᄑ',
        'r': 'ᄅ',
        't': 'ᄐ',
        'w': 'ᄇ',
        'ŋ': 'ᄉ',
        'ƒ': 'ᄌ',
        'x': 'ᄋ'
    }

    decoder_dict = {v: k for k, v in encoder_dict.items()}

    def preprocess(self, text):
        return Base().encode(text).lower()

    def tokenize(self, text):
        for i, ch in enumerate(text):
            if ch not in _vowels.union(_consonants):
                yield ch
            elif ch in _vowels and text[i - 1] not in _consonants:
                # ch is a vowel and the preceding char is not a consonant
                yield ch
            elif ch in _consonants:
                # ch is a consonant
                yield text[i:i + 2]

    def encode(self, text):
        text = self.preprocess(text)
        text_encoded = []
        for syllable in self.tokenize(text):
            if syllable in [" ", "-"]:
                text_encoded.append(syllable)
                continue
            if len(syllable) == 1:
                if syllable in _vowels.union(_consonants):
                    syllable = 'x' + syllable
                else:
                    text_encoded.append(syllable)
                    continue
            try:
                consonant, vowel = ''.join(
                    [self.encoder_dict[ch] for ch in syllable])
            except KeyError:
                logging.error(
                    "KeyError: phoneme {} in sent {} not in encoder_dict".
                    format(syllable, text))
                raise KeyError
            try:
                encoded = jamo.j2h(consonant, vowel)
            except jamo.InvalidJamoError:
                logging.error(
                    'InvalidJamoError - Consonant={} Vowel={} Syllable={} Sent={}'
                    .format(consonant, vowel, syllable, text[:100]))
            text_encoded.append(encoded)
        return ''.join(text_encoded)

    def decode(self, text):
        decoded_sent = ''
        for ch in text:
            if jamo.is_hangul_char(ch):
                decoded_sent += ''.join(
                    [self.decoder_dict[ch] for ch in jamo.hangul_to_jamo(ch)])
            else:
                decoded_sent += ch

        decoded_sent = decoded_sent.replace('x', '')
        decoded_sent = decoded_sent.replace('ŋ', 'ng')
        decoded_sent = decoded_sent.replace('ƒ', 'wh')

        return decoded_sent
