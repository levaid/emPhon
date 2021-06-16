import re
import json
import os
from typing import List

MAIN_POS = {'/V', '/N', '/Adj', '/Adv'}


class Transcriber:
    """
    Phonetic transcriber class. Examples are commented after the rules to ease the reading of regexes.
    """
    def __init__(self, ipaize: bool = True, optional_palatal_assimilation: bool = False):
        """
        :param ipaize: whether the output uses the inner representation or the IPA form
        :param optional_palatal_assimilation: optional palatal assimilation in cases like `lapátnyél`
        """
        self.optional_palatal_assimilation = optional_palatal_assimilation

        self.ipaize = ipaize
        if self.ipaize:
            with open(os.path.join(os.path.dirname(__file__), 'ipa_key.json')) as infile:
                self.ipa_key = json.load(infile)

        self.double_letter_vocab = {
            'ccs': 'Č',
            'ddzs': 'Ĵ',
            'ddz': 'Ď',
            'ggy': 'Ǧ',
            'lly': 'J',
            'nny': 'Ɲ',
            'ssz': 'Ʃ',
            'tty': 'Ť',
            'zzs': 'Ž',
            'cs': 'č',
            'dzs': 'ĵ',
            'dz': 'ď',
            'gy': 'ǧ',
            'ly': 'j',
            'ny': 'ɲ',
            'sz': 'ʃ',
            'ty': 'ť',
            'zs': 'ž'}

    def __call__(self, sentence: str, passes=2) -> str:
        """
        Processes the incoming strings. Does `passes` passes so that a rule can feed into another rule.
        :param sentence: the sentence to process
        :param passes: the number of passes sentence goes under
        :return: the processed sentence
        """
        sentence = self.x_letter(sentence)
        sentence = self.double_letters(sentence)
        sentence = self.h_transformation(sentence)
        sentence = self.hiatus_filling(sentence)

        for _ in range(passes):

            sentence = self.n_nasalization(sentence)
            sentence = self.l_assimilation(sentence)
            sentence = self.degemination(sentence)
            sentence = self.n_assimilation(sentence)
            sentence = self.palatal_assimilation(sentence)
            sentence = self.m_nasalization(sentence)
            sentence = self.sibilant_assimilation(sentence)
            sentence = self.voice_assimilation(sentence)
            sentence = self.nasalisation(sentence)

        if self.ipaize:
            return self.ipaization(sentence)
        else:
            return sentence

    @staticmethod
    def x_letter(sentence: str) -> str:
        return re.sub(r'[Xx]', 'ksz', sentence)

    @staticmethod
    def _long_letters(sentence: str) -> str:
        sentence = re.sub(r'([bcdfghjklmnpqrstvxzčďǧɲʃťž])\1',
                          lambda m: m.group(1).upper(), sentence)
        return sentence

    @staticmethod
    def _stronger_long_letters(sentence: str) -> str:
        sentence = re.sub(r'([bcdfghjklmnpqrstvxzčďǧɲʃťž])[|~§#]?\1',
                          lambda m: m.group(1).upper(), sentence)
        return sentence

    def double_letters(self, sentence: str) -> str:

        sentence = re.sub(r'(ccs|ddzs|ddz|ggy|lly|nny|ssz|tty|zzs|cs|dzs|dz|gy|ly|ny|sz|ty|zs)',
                          lambda m: self.double_letter_vocab[m.group(1)], sentence)

        sentence = self._long_letters(sentence)

        return sentence

    def l_assimilation(self, sentence: str) -> str:
        sentence = re.sub(r'[lL][|§#~]?r', r'R', sentence)  # balra
        return self.double_letters(sentence)

    def h_transformation(self, sentence: str) -> str:
        sentence = re.sub(r'(ch$)', r'Ḧ', sentence)
        sentence = re.sub(
            r'([aáeéiíoóöőüűuú][|§#~ ]?)h([|§#~ ]?[aáeéiíoóöőüűuú])', r'\g<1>ɦ\g<2>', sentence)  # tehén
        sentence = re.sub(
            r'([aáeéiíoóöőüűuú][|§#~ ]?)H([|§#~ ]?[aáeéiíoóöőüűuú])', r'\g<1>Ḧ\g<2>', sentence)  # ahhoz
        sentence = re.sub(
            r'([aáeéiíoóöőüűuú][|§#~]?)[c]h([|§#~]?[bcdfgjklmnpqrstvxzčďǧɲʃťž ]?)', r'\g<1>ḧ\g<2>', sentence)  # pechből
        sentence = re.sub(r'([mnɲrlj][|§#~]?)h', r'\g<1>ɦ', sentence)

        return self._long_letters(sentence)

    def nasalisation(self, sentence: str) -> str:
        pairs = {'p': 'm', 'b': 'm', 'f': 'm', 'v': 'm', 'ǧ': 'ɲ', 'ť': 'ɲ'}
        sentence = re.sub(r'n([|~§#]?)([pbfvǧť])', lambda m: pairs[m.group(
            2)]+m.group(1)+m.group(2), sentence)  # tanpálya
        sentence = re.sub(r'(n)([|~§#]?ɲ)', r'Ɲ', sentence)  # lennyakkendő
        return self._long_letters(sentence)

    def n_assimilation(self, sentence: str) -> str:
        sentence = re.sub(r'n[|~§]?([lr])',
                          lambda m: m.group(1).upper(), sentence)  # hasonló
        return self._long_letters(sentence)

    def sibilant_assimilation(self, sentence: str) -> str:
        sentence = re.sub(r'(t)([|~§#]?ʃ)', r'C', sentence)  # hatszög
        sentence = re.sub(r'(t)([|~§#]?s)', r'Č', sentence)  # hátság
        sentence = re.sub(r'(t)([|~§# ]?c)', r'C', sentence)  # hét cica
        sentence = re.sub(r'(t)([|~§# ]?č)', r'Č', sentence)  # hat csap
        sentence = re.sub(r'(d)([|~§#]?ʃ)', r'C', sentence)  # rendszer
        sentence = re.sub(r'(d)([|~§#]?s)', r'Č', sentence)  # hadsereg
        return self._long_letters(sentence)

    def voice_assimilation(self, sentence: str) -> str:
        # voiced = 'bdǧgzžď'
        # voiceless = 'ptťkʃscf'
        pairs = {'p': 'b', 'b': 'p', 't': 'd', 'd': 't', 'ť': 'ǧ', 'ǧ': 'ť', 'k': 'g', 'g': 'k', 'f': 'v', 'v': 'f',
                 'ʃ': 'z', 'z': 'ʃ', 's': 'ž', 'ž': 's', 'c': 'ď', 'ď': 'c', 'h': 'ɦ', 'č': 'ĵ', 'ĵ': 'č'}

        sentence = re.sub(r'([bdǧgzžďvĵ])([|~§#]?[ptťkʃscfhč])',
                          lambda m: pairs[m.group(1)]+m.group(2), sentence)  # útpadka -> útpatka

        sentence = re.sub(r'([ptťkʃscfhč])([|~§#]?[bdǧgzžďĵ])',
                          lambda m: pairs[m.group(1)]+m.group(2), sentence)  # habfürdő -> hapfürdő

        return self._long_letters(sentence)

    def palatal_assimilation(self, sentence: str) -> str:
        # Rules in human-readable form
        # full = [
        #     ('ǧ', 'j', 'Ǧ'),
        #     ('d', 'j', 'Ǧ'),
        #     ('l', 'j', 'J'),
        #     ('n', 'j', 'Ɲ'),
        #     ('ɲ', 'j', 'Ɲ'),
        #     ('t', 'j', 'Ť'),
        #     ('ť', 'j', 'Ť')]
        # partial = [('d', 'ǧ', 'Ǧ'), ('t', 'ǧ', 'Ǧ'),
        #            ('d', 'ť', 'Ť'), ('t', 'ť', 'Ť')]
        # optional = [('d', 'ɲ', 'ǧɲ'), ('t', 'ɲ', 'ťɲ')]

        full_dict = {'ǧ': 'Ǧ', 'd': 'Ǧ', 'l': 'J',
                     'n': 'Ɲ', 'ɲ': 'Ɲ', 't': 'Ť', 'ť': 'Ť'}
        # partial is [dt][ǧť] and the second is upper
        optional_dict = {'d': 'ǧɲ', 't': 'ťɲ'}

        sentence = re.sub(r'([ǧdlnɲtť])[|~§#]?j',
                          lambda m: full_dict[m.group(1)], sentence)  # hagyjál

        sentence = re.sub(r'[dt][|~§# ]?([ǧť])',
                          lambda m: m.group(1).upper(), sentence)  # hét tyúk

        if self.optional_palatal_assimilation:
            sentence = re.sub(r'([dt])[|~§# ]?ɲ',
                              lambda m: optional_dict[m.group(1)], sentence)  # lapátnyél

        return self._long_letters(sentence)

    @staticmethod
    def hiatus_filling(sentence: str) -> str:
        sentence = re.sub(r'i[|~§]?([aáeéoóöőüűuú])', r'ij\g<1>', sentence)
        sentence = re.sub(r'([aáeéoóöőüűuú])[|~§]?i', r'\g<1>ji', sentence)
        return sentence

    def n_nasalization(self, sentence: str) -> str:
        sentence = re.sub(r'n[|~§#]?([gk])', r'ŋ\g<1>', sentence)
        return self.double_letters(sentence)

    def degemination(self, sentence: str) -> str:
        # These are left here intentionally, for reference.
        # consonants = 'bcdfghjklmnpqrstvwxzčďǧɲʃťž'
        # long_consonants = 'BCDFGHJKLMNPQRSTVWXZČĎǦƝƩŤŽ'
        # liquid = 'jlr'
        # nasal = 'mnɲ'
        # obstruents = 'bcdfghkpqstvwxzčďǧʃťž'

        # short consonant after long consonant
        sentence = re.sub(r'([BCDFGHJKLMNPQRSTVWXZČĎǦƝƩŤŽ])([|§~# ]?)([bcdfghjklmnpqrstvwxzčďǧɲʃťž])',
                          lambda m: m.group(1).lower()+m.group(2)+m.group(3), sentence)  # Ludd tábornok

        # short#1 short#2 short#2
        sentence = re.sub(r'([bcdfghjklmnpqrstvwxzčďǧɲʃťž]([bcdfghjklmnpqrstvwxzčďǧɲʃťž]))[|#§~ ]?\2',
                          r'\g<1>', sentence)  # Ford dísztárcsa

        # short long
        sentence = re.sub(r'([bcdfghjklmnpqrstvwxzčďǧɲʃťž])[|~#§]?([BCDFGHJKLMNPQRSTVWXZČĎǦƝƩŤŽ])',
                          lambda m: m.group(1)+m.group(2).lower(), sentence)  #

        # cons#1 cons#1 obstruent
        sentence = re.sub(
            r'([bcdfghjklmnpqrstvwxzčďǧɲʃťž])[|~#§ ]?(\1[bcdfghkpqstvwxzčďǧʃťž])', r'\g<2>', sentence)

        # long cons obstruent
        sentence = re.sub(r'([BCDFGHJKLMNPQRSTVWXZČĎǦƝƩŤŽ])([bcdfghkpqstvwxzčďǧʃťž])',
                          lambda m: m.group(1).lower()+m.group(2), sentence)

        # cons cons nasal
        sentence = re.sub(
            r'([bcdfghjklmnpqrstvwxzčďǧɲʃťž])[|~#§ ]?(\1[mnɲ])', r'\g<2>', sentence)  # optional

        # long cons nasal
        sentence = re.sub(r'([BCDFGHJKLMNPQRSTVWXZČĎǦƝƩŤŽ])([mnɲ])', lambda m: m.group(
            1).lower()+m.group(2), sentence)

        return self._long_letters(sentence)

    def m_nasalization(self, sentence: str) -> str:
        sentence = re.sub(r'[mn][|#§~ ]?([fv])', r'ɱ\g<1>', sentence)  # kámfor
        return self._long_letters(sentence)

    def ipaization(self, sentence: str) -> str:
        sentence = self._long_letters(re.sub(r'[|~§#]', '', sentence))
        ipa_sentence = ''.join(self.ipa_key.get(letter, letter) for letter in sentence)
        return ipa_sentence

    @staticmethod
    def segment(sentence: List[List[str]], field_names: dict) -> List[str]:
        """
        Segment words based on morphological analysis. It uses the field `anas`, which contains the output of emMorph
        with the possible segmentation. Selects the longest analysis (which is supposedly the finest), then adds
        delimiters based on the morph boundaries. In case of no analysis, it assumes that the token is a single morph.
        :param sentence: xtsv sentence with `form` and `morph` fields
        :param field_names: field names
        :return: list of segmented words
        """
        new_sentence = []

        for line in sentence:
            anas = json.loads(line[field_names['anas']])
            #  we suppose that the longest morphana is the finest
            anas_sorted = [ana['morphana']
                           for ana in sorted(anas, key=lambda s: s['morphana'].count('+'), reverse=True)]
            #  in case it is a symbol or some other weird thing the morphana is empty
            if anas_sorted == [] or anas_sorted == ['']:
                new_sentence.append(line[field_names['form']].lower() + ' ')
            else:
                #  the regex finds tag-surface realization pairs
                tags, morphs, _ = zip(*re.findall(r"\[(.*?)\]=(.*?)(\+|$)", anas_sorted[0]))
                morphs = [x.lower() for x in morphs]
                #  in some special cases like adverbs, punctiations there is only one morph and we have to consider it #
                #  a special case
                if len(morphs) == 1:
                    new_sentence.append(morphs[0] + ' ')
                else:
                    word = []
                    is_end_of_main = False
                    #  we iterate over the morphs and make 4 distinct categories:
                    #  before root, between roots, after root, between suffixes
                    #  we mark these by | # § ~
                    #  and for the empty morphs in the Hungarian at the end of words (Nom), we discard it
                    for i, morph in enumerate(morphs[:-1]):
                        word.append(morph)
                        if morphs[i+1] == '':
                            continue  # to avoid empty | in the end
                        curr_is_lemma, next_is_lemma = tags[i] in MAIN_POS, tags[i+1] in MAIN_POS
                        if is_end_of_main:
                            word.append('|')
                        elif curr_is_lemma and next_is_lemma:
                            word.append('#')
                        elif not curr_is_lemma and next_is_lemma:
                            word.append('§')
                        elif curr_is_lemma and not next_is_lemma:
                            word.append('~')
                            is_end_of_main = True
                        elif not curr_is_lemma and not next_is_lemma:
                            word.append('|')
                    else:
                        if morphs[-1] != '':  # empty morphemes at the end (nominative suffix) have to be discarded
                            word.append(morphs[-1])

                    new_sentence.append(''.join(word + [' ']))

        return new_sentence
