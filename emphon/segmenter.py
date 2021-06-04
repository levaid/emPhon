import json
import re
from typing import List


class Segmenter:
    def __init__(self):
        self.MAIN_POS = {'/V', '/N', '/Adj', '/Adv'}

    def segment(self, sentence: List[str], field_names: dict) -> List[str]:

        new_sentence = []

        for line in sentence:
            anas = json.loads(line[field_names['anas']])
            #  we suppose that the longest morphana is the finest
            anas_sorted = [ana['morphana'] for ana in sorted(anas, key=lambda s: s['morphana'].count('+'), reverse=True)]
            if anas_sorted == [] or anas_sorted == ['']:  # in case it is a symbol or some other weird thing
                new_sentence.append(line[0].lower() + ' ')
            else:
                #  the regex finds tag-surface realization pairs
                tags, morphs, _ = zip(*re.findall(r"\[(.*?)\]=(.*?)(\+|$)", anas_sorted[0]))
                morphs = [x.lower() for x in morphs]
                if len(morphs) == 1:
                    new_sentence.append(morphs[0] + ' ')
                    pass
                else:
                    word = []
                    is_end_of_main = False
                    for i, _ in enumerate(morphs[:-1]):
                        word.append(morphs[i])
                        if morphs[i+1] == '':
                            continue  # to avoid empty | in the end
                        curr_is_lemma, next_is_lemma = tags[i] in self.MAIN_POS, tags[i+1] in self.MAIN_POS
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
                        if morphs[-1] != '':  # empty morphemes at the end (like nominative suffix) have to be discarded
                            word.append(morphs[-1])

                    new_sentence.append(''.join(word) + ' ')

        return new_sentence
