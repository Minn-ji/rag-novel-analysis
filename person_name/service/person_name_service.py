from tqdm import tqdm
from person_name.repository.person_name_repository import PersonNameRepository
from person_name.repository.person_name_roberta_repository import PersonNameRoBERTaRepository
from person_name.repository.person_name_konlpy_repository import PersonNameKonlpyRepository

class PersonNameService:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__personNameRepository = PersonNameRepository.getInstance()
            cls.__instance.__personNameRoBERTaRepository = PersonNameRoBERTaRepository.getInstance()
            cls.__instance.__personNameKonlpyRepository = PersonNameKonlpyRepository.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    def extract_person_name_with_RoBERTa(self, splitted_texts, min_n, max_n, step):
        extracted_names = self.__personNameRoBERTaRepository.extract_PS_token(splitted_texts)

        name_map = self.__personNameRepository.get_name_map(extracted_names)
        
        for n in range(min_n, max_n, step):
            main_character_names = self.__personNameRepository.filter_n_names(name_map, n)
            self.__personNameRepository.generate_wordcloud(main_character_names, image_name=f'roberta_person_{n}')
            main_character_names = list(main_character_names.keys())
            self.__personNameRepository.save_name_result(main_character_names, n, roberta=True)


    def extract_person_name_with_Kkma(self, splitted_texts, min_n, max_n, step):
        extracted_nouns = []
        for text in tqdm(splitted_texts, desc='get person name with Kkma'):
            tokens = self.__personNameKonlpyRepository.get_nouns(text)
            extracted_nouns.extend(tokens)

        name_map = self.__personNameRepository.get_name_map(extracted_nouns)
        
        for n in range(min_n, max_n, step):
            main_character_names = self.__personNameRepository.filter_n_names(name_map, n)
            self.__personNameRepository.generate_wordcloud(main_character_names, image_name=f'kkma_person_{n}')
            main_character_names = list(main_character_names.keys())
            self.__personNameRepository.save_name_result(main_character_names, n, roberta=False)