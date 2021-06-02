import re


class Transcriber():
    """
    Phonetic transcriber class. Examples are commented after the rules to ease the reading of regexes.
    """
    def __init__(self, optional_palatal_assimilation: bool = False):
        self.optional_palatal_assimilation = optional_palatal_assimilation

    def process(self, sentence: str, ipaize: bool = True) -> str:
        sentence = self.double_letters(sentence)
        sentence = self.h_transformation(sentence)
        sentence = self.degemination(sentence)
        sentence = self.n_assimilation(sentence)
        sentence = self.palatal_assimilation(sentence)
        sentence = self.m_nasalization(sentence)
        sentence = self.sibilant_assimilation(sentence)
        sentence = self.voice_assimilation(sentence)
        sentence = self.nasalisation(sentence)

        sentence = self.hiatus_filling(sentence)
        sentence = self.n_nasalization(sentence)
        sentence = self.l_assimilation(sentence)
        sentence = self.degemination(sentence)
        sentence = self.n_assimilation(sentence)
        sentence = self.palatal_assimilation(sentence)
        sentence = self.sibilant_assimilation(sentence)
        sentence = self.voice_assimilation(sentence)
        sentence = self.nasalisation(sentence)

        if ipaize:
            return(self.ipaization(sentence))
        else:
            return(sentence)

    def x_letter(self, sentence: str):
        return re.sub(r'[Xx]', 'ksz', sentence)
        # return(sentence.replace('x', 'ksz').replace('X', 'ksz'))

    def long_letters(self, sentence: str):
        sentence = re.sub(r'([bcdfghjklmnpqrstvxzčďǧɲʃťž])\1',
                          lambda m: m.group(1).upper(), sentence)
        return(sentence)

    def stronger_long_letters(self, sentence: str):
        sentence = re.sub(r'([bcdfghjklmnpqrstvxzčďǧɲʃťž])[|~§#]?\1',
                          lambda m: m.group(1).upper(), sentence)
        return(sentence)

    def double_letters(self, sentence: str):
        double_long = [('ccs', 'Č'), ('ddzs', 'Ĵ'), ('ddz', 'Ď'), ('ggy', 'Ǧ'),
                       ('lly', 'J'), ('nny', 'Ɲ'), ('ssz', 'Ʃ'), ('tty', 'Ť'), ('zzs', 'Ž')]
        double = [('cs', 'č'), ('dzs', 'ĵ'), ('dz', 'ď'), ('gy', 'ǧ'),
                  ('ly', 'j'), ('ny', 'ɲ'), ('sz', 'ʃ'), ('ty', 'ť'), ('zs', 'ž')]

        double_letters = dict(double + double_long)

        sentence = re.sub(r'(ccs|ddzs|ddz|ggy|lly|nny|ssz|tty|zzs|cs|dzs|dz|gy|ly|ny|sz|ty|zs)',
                          lambda m: double_letters[m.group(1)], sentence)

        sentence = self.long_letters(sentence)

        return(sentence)

    def l_assimilation(self, sentence: str):
        sentence = re.sub(r'[lL][|§#~]?r', r'R', sentence)  # balra
        return(self.double_letters(sentence))

    def h_transformation(self, sentence: str):
        sentence = re.sub(r'(ch$)', r'Ḧ', sentence)
        sentence = re.sub(
            r'([aáeéiíoóöőüűuú][|§#~ ]?)h([|§#~ ]?[aáeéiíoóöőüűuú])', r'\g<1>ɦ\g<2>', sentence)  # tehén
        sentence = re.sub(
            r'([aáeéiíoóöőüűuú][|§#~ ]?)H([|§#~ ]?[aáeéiíoóöőüűuú])', r'\g<1>Ḧ\g<2>', sentence)  # ahhoz
        sentence = re.sub(
            r'([aáeéiíoóöőüűuú][|§#~]?)[c]h([|§#~]?[bcdfgjklmnpqrstvxzčďǧɲʃťž ]?)', r'\g<1>ḧ\g<2>', sentence)  # pechből
        sentence = re.sub(r'([mnɲrlj][|§#~]?)h', r'\g<1>ɦ', sentence)

        return(self.long_letters(sentence))

    def nasalisation(self, sentence: str):
        pairs = {'p': 'm', 'b': 'm', 'f': 'm', 'v': 'm', 'ǧ': 'ɲ', 'ť': 'ɲ'}
        sentence = re.sub(r'n([|~§#]?)([pbfvǧť])', lambda m: pairs[m.group(
            2)]+m.group(1)+m.group(2), sentence)  # tanpálya
        sentence = re.sub(r'(n)([|~§#]?ɲ)', r'Ɲ', sentence)  # lennyakkendő
        return(self.long_letters(sentence))

    def n_assimilation(self, sentence: str):
        sentence = re.sub(r'n[|~§]?([lr])',
                          lambda m: m.group(1).upper(), sentence)  # hasonló
        return(self.long_letters(sentence))

    def sibilant_assimilation(self, sentence: str):
        sentence = re.sub(r'(t)([|~§#]?ʃ)', r'C', sentence)  # hatszög
        # sentence = re.sub(r'(d)([|~§]?z)',r'R',sentence) is 'dz' long or not in every situation?
        sentence = re.sub(r'(t)([|~§#]?s)', r'Č', sentence)  # hátság
        sentence = re.sub(r'(t)([|~§# ]?c)', r'C', sentence)  # hét cica
        sentence = re.sub(r'(t)([|~§# ]?č)', r'Č', sentence)  # hat csap
        sentence = re.sub(r'(d)([|~§#]?ʃ)', r'C', sentence)  # rendszer
        sentence = re.sub(r'(d)([|~§#]?s)', r'Č', sentence)  # hadsereg
        return(self.long_letters(sentence))

    def voice_assimilation(self, sentence: str):
        # voiced = 'bdǧgzžď'
        # voiceless = 'ptťkʃscf'
        pairs = {'p': 'b', 'b': 'p', 't': 'd', 'd': 't', 'ť': 'ǧ', 'ǧ': 'ť', 'k': 'g', 'g': 'k', 'f': 'v', 'v': 'f',
                 'ʃ': 'z', 'z': 'ʃ', 's': 'ž', 'ž': 's', 'c': 'ď', 'ď': 'c', 'h': 'ɦ', 'č': 'ĵ', 'ĵ': 'č'}

        sentence = re.sub(r'([bdǧgzžďvĵ])([|~§#]?[ptťkʃscfhč])',
                          lambda m: pairs[m.group(1)]+m.group(2), sentence)  # HACK h

        sentence = re.sub(r'([ptťkʃscfhč])([|~§#]?[bdǧgzžďĵ])',
                          lambda m: pairs[m.group(1)]+m.group(2), sentence)  # HACK h

        return(self.long_letters(sentence))

    def palatal_assimilation(self, sentence: str):
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

        return(self.long_letters(sentence))

    def hiatus_filling(self, sentence: str):
        sentence = re.sub(r'i[|~§]?([aáeéoóöőüűuú])', r'ij\g<1>', sentence)
        sentence = re.sub(r'([aáeéoóöőüűuú])[|~§]?i', r'\g<1>ji', sentence)
        return(sentence)

    def n_nasalization(self, sentence: str):
        sentence = re.sub(r'n[|~§#]?([gk])', r'ŋ\g<1>', sentence)
        return(self.double_letters(sentence))

    def degemination(self, sentence: str):
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
        sentence = re.sub(
            r'([bcdfghjklmnpqrstvwxzčďǧɲʃťž]([bcdfghjklmnpqrstvwxzčďǧɲʃťž]))[|#§~ ]?\2', r'\g<1>', sentence)  # Ford dísztárcsa

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

        return(self.long_letters(sentence))

    def m_nasalization(self, sentence: str):
        sentence = re.sub(r'[mn][|#§~ ]?([fv])', r'ɱ\g<1>', sentence)  # kámfor
        return(self.long_letters(sentence))

    def ipaization(self, sentence: str):
        ipa_sentence = ''
        ipa = {'a': 'ɒ', 'á': 'aː', 'b': 'b', 'c': 't͡s', 'č': 't͡ʃ', 'd': 'd', 'ď': 'd͡z', 'e': 'ɛ',
               'é': 'eː', 'f': 'f', 'g': 'ɡ', 'ǧ': 'ɟ', 'h': 'h', 'i': 'i', 'í': 'iː', 'j': 'j',
               'k': 'k', 'l': 'l', 'ly': 'j', 'm': 'm', 'n': 'n', 'ɲ': 'ɲ', 'o': 'o', 'ó': 'oː',
               'ö': 'ø', 'ő': 'øː', 'p': 'p', 'q': 'k', 'r': 'r', 's': 'ʃ', 'ʃ': 's', 't': 't',
               'ť': 'c', 'u': 'u', 'ú': 'uː', 'ü': 'y', 'ű': 'yː', 'v': 'v', 'w': 'v', 'x': 'ks',
               'y': 'i', 'z': 'z', 'ž': 'ʒ', 'B': 'bː', 'C': 't͡sː', 'Č': 't͡ʃː', 'D': 'dː', 'Ď': 'd͡zː',
               'F': 'fː', 'G': 'ɡː', 'Ǧ': 'ɟː', 'H': 'hː', 'J': 'jː', 'K': 'kː', 'L': 'lː', 'ly': 'j',
               'M': 'mː', 'N': 'nː', 'Ɲ': 'ɲː', 'P': 'pː', 'Q': 'kː', 'R': 'rː', 'S': 'ʃː', 'Ʃ': 'sː',
               'T': 'tː', 'Ť': 'cː', 'V': 'vː', 'W': 'vː', 'X': 'ksː', 'Z': 'zː', 'Ž': 'ʒː', 'Ḧ': 'xː',
               'ḧ': 'x', 'ĵ': 'd͡ʒ', 'ď': 'd͡z', 'Ĵ': 'd͡ʒː', 'Ď': 'd͡zː'}

        sentence = self.long_letters(re.sub(r'[|~§#]', '', sentence))
        for letter in sentence:
            ipa_sentence += ipa.get(letter, letter)

        return(ipa_sentence)
