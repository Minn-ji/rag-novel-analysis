import os
from person_name.service.person_name_service import PersonNameService
from util.text_preprocessing import load_data, split_texts, save_result


def extract_person_name():
    __personNameService = PersonNameService.getInstance()
    texts = load_data('data/상록수_심대섭.txt')
    splitted_texts = split_texts(texts)

    __personNameService.extract_person_name_with_RoBERTa(splitted_texts, 10,46,5)
    # __personNameService.extract_person_name_with_Kkma(splitted_texts, 10,46,5)
    

if __name__ == '__main__':
    extract_person_name()
### python -m person_name.person_name_controller