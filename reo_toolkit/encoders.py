import re
import nltk
import jamo
import logging

from .utils import pairwise

_vowels = list('aeiouāēīōū')
_consonants = list("hkmnprtwŋƒ")


class NoEncoder:
    def encode(self, text):
        return text

    def decode(self, text):
        return text


class BaseEncoder:
    def encode(self, text):
        return text.replace('ng', 'ŋ').replace('wh', 'ƒ')

    def decode(self, text):
        return text.replace('ŋ', 'ng').replace('ƒ', 'wh')


class ShortmoraEncoder:

    encoder_dict = {
        'ā': 'aa',
        'ē': 'ee',
        'ī': 'ii',
        'ō': 'oo',
        'ū': 'uu',
        'ng': 'ŋ',
        'wh': 'ƒ'
    }

    decoder_dict = {v: k for k, v in encoder_dict.items()}

    def encode(self, text):
        for k, v in self.encoder_dict.items():
            text = text.replace(k, v)
        return text

    def decode(self, text):
        for k, v in self.decoder_dict.items():
            text = text.replace(k, v)
        return text


class MoraEncoder:

    encoder_dict = {
        'ae': 'æ',
        'ai': 'á',
        'ao': 'å',
        'au': 'ä',
        'ei': 'é',
        'eu': 'ë',
        'iu': 'ï',
        'oe': 'œ',
        'oi': 'ó',
        'ou': 'ö',
        'ng': 'ŋ',
        'wh': 'ƒ',
    }

    decoder_dict = {v: k for k, v in encoder_dict.items()}

    def encode(self, text):
        for k, v in self.encoder_dict.items():
            text = text.replace(k, v)
        return text

    def decode(self, encoded_text):
        for diphthong, mora in self.encoder_dict.items():
            encoded_text = encoded_text.replace(mora, diphthong)
        return encoded_text


class SyllableEncoder:

    encoder_dict = {
        'a': 'ᅡ',
        'h': 'ᄒ',
        'ā': 'ᅣ',
        'k': 'ᄏ',
        'e': 'ᅦ',
        'm': 'ᄆ',
        'ē': 'ᅨ',
        'n': 'ᄂ',
        'i': 'ᅥ',
        'p': 'ᄑ',
        'ī': 'ᅧ',
        'r': 'ᄅ',
        'o': 'ᅩ',
        't': 'ᄐ',
        'ō': 'ᅭ',
        'w': 'ᄇ',
        'u': 'ᅮ',
        'ŋ': 'ᄉ',
        'ū': 'ᅲ',
        'ƒ': 'ᄌ',
        'x': 'ᄋ'
    }

    decoder_dict = {v: k for k, v in encoder_dict.items()}

    def preprocess(self, text):
        return BaseEncoder().encode(text).lower()

    def tokenize(self, text):
        for i, ch in enumerate(text):
            if ch not in _vowels + _consonants:
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
                if syllable in _vowels + _consonants:
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
