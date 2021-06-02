from typing import List
from emphon.segmenter import Segmenter
from emphon.transcriber import Transcriber


class EmPhon:
    def __init__(self, source_fields=None, target_fields=None, transcriber_opts: dict = None, strict_xtsv_format=False):

        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        if transcriber_opts is None:
            transcriber_opts = dict()

        self.source_fields = source_fields
        self.target_fields = target_fields

        self.segmenter = Segmenter()
        self.transcriber = Transcriber(**transcriber_opts)

        if strict_xtsv_format:
            self.transcribe = self.transcribe_strict
        else:
            self.transcribe = self.transcribe_lax

    def transcribe_strict(self, segmented_sentence: List[str]) -> List[str]:
        """
        Use with caution. Transcribes sentences word-by-word, meaning the rules do not work over word limits.
        Its advantage is that it provides xtsv-like one word per line output.
        """
        return [self.transcriber.process(word) for word in segmented_sentence]

    def transcribe_lax(self, segmented_sentence: List[str]) -> List[str]:
        """
        Transcribes sentences by whole.
        The first word line of the sentence contains the whole phonetic form, the rest of the sentence is padded with `_`.
        """

        transcribed_sentence = self.transcriber.process(''.join(segmented_sentence))

        return [transcribed_sentence if i == 0 else '_' for i, _ in enumerate(segmented_sentence)]

    def process_sentence(self, sen, field_names=None):
        """
        Process one sentence per function call
        :param sen: The list of all tokens in the sentence, each token contain all fields
        :param field_names: The prepared field_names from prepare_fields() to select the appropriate input field
         to process
        :return: The sen object augmented with the output field values for each token
        """

        segmented_sentence = self.segmenter.segment(sentence=sen, field_names=field_names)

        transcribed_sentence = self.transcribe(segmented_sentence)

        for line, transcription in zip(sen, transcribed_sentence):
            line.append(transcription)

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

