from transformers import AutoTokenizer, AutoModel

from util.global_varb import sentence_embedding_model


class SentenceHelper:

    def __init__(self, sentences:list):
        self.tokenizer = None
        self.model = None
        self.sentence = sentences


    def get_sentence(self):
        return self.sentence

    def set_sentence(self, new_sentence):
        self.sentence = new_sentence

    def get_sentence_vector(self):
        if self.model is None:
            self.tokenizer = AutoTokenizer.from_pretrained(sentence_embedding_model)
            self.model = AutoModel.from_pretrained(sentence_embedding_model)
        return self.model.encode(self.sentence)