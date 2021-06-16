from typing import List
from emphon.transcriber import Transcriber


class EmPhon:
    def __init__(
            self, source_fields=None, target_fields=None, transcriber_opts: dict = None, strict_xtsv_format=False,
            include_sentence=False):

        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        if transcriber_opts is None:
            transcriber_opts = dict()

        self.source_fields = source_fields
        self.target_fields = target_fields

        self.transcriber = Transcriber(**transcriber_opts)

        self.include_sentence = include_sentence

    def comment_full_surface_form(self, segmented_sentence: List[str]) -> List[List[str]]:

        full_sentence = self.transcriber(''.join(segmented_sentence))

        return [['# phon = ' + full_sentence]]

    def process_sentence(self, sen, field_names=None):
        """
        Process one sentence per function call
        :param sen: The list of all tokens in the sentence, each token contain all fields
        :param field_names: The prepared field_names from prepare_fields() to select the appropriate input field
         to process
        :return: The sen object augmented with the output field values for each token
        """

        segmented_sentence = self.transcriber.segment(sentence=sen, field_names=field_names)

        per_word_sentence = [self.transcriber(word) for word in segmented_sentence]

        for line, transcription in zip(sen, per_word_sentence):
            line.append(transcription)

        if self.include_sentence:
            return self.comment_full_surface_form(segmented_sentence) + sen
        else:
            return sen

    @staticmethod
    def prepare_fields(field_names):
        """
        This function is called once before processing the input. It can be used to initialise field conversion classes
         to accomodate the current order of fields (eg. field to features)
        :param field_names: The dictionary of the names of the input fields mapped to their order in the input stream
        :return: The list of the initialised feature classes as required for process_sentence (in most cases the
         columnnumbers of the required field in the required order are sufficient
         e.g. return [field_names['form'], field_names['lemma'], field_names['xpostag'], ...] )
        """
        return field_names

