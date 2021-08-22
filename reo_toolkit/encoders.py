import re
import nltk
import jamo
import json
import logging
from collections import OrderedDict
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

from .letters import vowels, consonants, alphabet


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
        'wh': 'ƒ',
        'Ā': 'Aa',
        'Ē': 'Ee',
        'Ī': 'Ii',
        'Ō': 'Oo',
        'Ū': 'Uu',
        'NG': 'Ŋ',
        'WH': 'Ƒ'
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
        'AE': 'Æ',
        'AI': 'Á',
        'AO': 'Å',
        'AU': 'Ä',
        'EI': 'É',
        'OE': 'Œ',
        'OI': 'Ó',
        'OU': 'Ö',
        'NG': 'Ŋ',
        'WH': 'Ƒ',
    }

    decoder_dict = {v: k for k, v in encoder_dict.items()}

    def tokenize(self, text):
        while len(text) > 0:
            if not text[0] in alphabet:
                yield text[0]
                text = text[1:]
            elif text[0] in consonants:
                yield text[0]
                text = text[1:]
            elif text[0] in vowels:
                if len(text) > 1 and text[1] in vowels:
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
            for mora in self.tokenize(sent):
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

    def __init__(self, vowel_type = 'long'):
        self.vowel_type = vowel_type

    def preprocess(self, text, vowel_type):
        # Syllable encoder only supports lowercase text
        text = text.lower()
        if vowel_type == 'short':
            text = SingleVowel().encode(text)
        return Base().encode(text)

    def tokenize(self, text):
        for i, ch in enumerate(text):
            if ch not in alphabet:
                yield ch
            elif ch == '-':
                yield ch
            elif ch in vowels and text[i-1] not in consonants:
                # ch is a vowel and the preceding char is not a consonant
                yield ch
            elif ch in consonants:
                # ch is a consonant
                yield text[i:i+2]

    def encode(self, text):
        text = self.preprocess(text, vowel_type = self.vowel_type)
        words = []
        for word in TreebankWordTokenizer().tokenize(text):
            from reo_toolkit import is_maori
            if not is_maori(word):
                words.append(word)
                continue
            encoded_text = []
            for syllable in self.tokenize(word):
                if not all(ch in alphabet for ch in syllable):
                    encoded_text.append(syllable)
                    continue
                if syllable in vowels:
                    syllable = 'x' + syllable
                try:
                    consonant, vowel = ''.join([self.encoder_dict[ch] for ch in syllable])
                except KeyError:
                    logging.error("KeyError: phoneme {} not in encoder_dict".format(syllable))
                    raise KeyError
                try:
                    encoded = jamo.j2h(consonant, vowel)
                except jamo.InvalidJamoError:
                    logging.error('InvalidJamoError - Consonant={} Vowel={} Syllable={}'.format(consonant, vowel, syllable))
                encoded_text.append(encoded)
            words.append(''.join(encoded_text))
        return TreebankWordDetokenizer().detokenize(words)

    def decode(self, encoded_text):
        decoded_sent = ''
        for ch in encoded_text:
            if jamo.is_hangul_char(ch):
                decoded_sent += ''.join([self.decoder_dict[ch] for ch in jamo.hangul_to_jamo(ch)])
            else:
                decoded_sent += ch
        decoded_sent = decoded_sent.replace('x', '').replace('ŋ', 'ng').replace('ƒ', 'wh')
        return decoded_sent


class DoubleVowel:

    def __init__(self):
        self.encoder_dict = json.load(open('reo_toolkit/double_vowel.json', 'r'), object_pairs_hook=OrderedDict)
        self.decoder_dict = {v:k for k,v in self.encoder_dict.items()}

    def encode(self, text):
        text = Base().encode(text)
        for syllable in self.encoder_dict:
            text = text.replace(syllable, self.encoder_dict[syllable])
        return text

    def decode(self, encoded):
        decoded = ''
        for ch in encoded:
            try:
                decoded += Base().decode(self.decoder_dict[ch])
            except KeyError:
                decoded += ch
        return decoded


class LongSyllable:

    def __init__(self):
        self.encoder_dict = json.load(open('reo_toolkit/long_syllable.json', 'r'), object_pairs_hook=OrderedDict)
        self.decoder_dict = {v:k for k,v in self.encoder_dict.items()}

    def encode(self, text):
        text = Base().encode(text)
        for syllable in self.encoder_dict:
            text = text.replace(syllable, self.encoder_dict[syllable])
        return text

    def decode(self, encoded):
        decoded = ''
        for ch in encoded:
            try:
                decoded += Base().decode(self.decoder_dict[ch])
            except KeyError:
                decoded += ch
        return decoded
