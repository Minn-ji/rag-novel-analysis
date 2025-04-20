from konlpy.tag import Kkma, Komoran, Okt
from util.text_preprocessing import load_data, split_texts


class PersonNameKonlpyRepository:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            return cls.__instance
    
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def word_tagging(self, text):
        kkma = Kkma()
        return kkma.pos(text)

    def word_tagging_komoran(self, text):
        komoran = Komoran()
        return komoran.pos(text)
    
    def word_tagging_okt(self, text):
        okt = Okt()
        return okt.pos(text)
        

    def get_nouns(self, text):
        kkma = Kkma()
        return [word for (word, tag) in kkma.pos(text) if tag in ('NNG', 'NNP')]


if __name__ == '__main__':
    texts = load_data('data/상록수_심대섭.txt')
    splitted_texts = split_texts(texts)
    names = []
    for text in splitted_texts:
        print(text)
        word_tagging(text)

        print('======================')
    