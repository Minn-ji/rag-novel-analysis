import chardet
import json
import re
from util.hanspell import spell_checker

def detect_encoding(filename):
    with open(filename, "rb") as f:
        raw_data = f.read()
    return chardet.detect(raw_data)["encoding"]

def load_json_data(file_path):
    with open(file_path, 'r', encoding=detect_encoding(file_path)) as f:
        contents = json.load(f)
    return contents

def save_dict_result(dict_data, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(dict_data, file, ensure_ascii=False, indent=4)
        print(f'{file_name} save 완료')

def load_data(file_path):
    with open(file_path, encoding=detect_encoding(file_path)) as f:
        contents = f.read()
    return contents

def save_result(data, file_name='saved_result.json'):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(list(data), file, ensure_ascii=False, indent=4)
    print(f'{file_name} save 완료')


def remove_stopwords(texts):
    stopword_chars = '―-"\'.,’…~`@*:;/\\|_&%(){}[]#' 
    pattern = '[' + re.escape(stopword_chars) + ']'
    filtered_texts = [re.sub(pattern, '', text) for text in texts]

    return filtered_texts


def split_texts(texts):
    texts = texts.replace('.', '.<s>')
    texts = texts.replace('?', '?<s>')
    texts = texts.replace('!', '!<s>')
    texts = texts.replace(',\n "', '<s>')
    texts = texts.replace('고농', '고등농림학교')
    texts = texts.replace('\n', '')
    texts = texts.replace('  ', '')
    texts = re.sub(r'\([^)]*\)', '', texts)
    texts = texts.split('<s>')
    texts = remove_stopwords(texts)
    return texts


def spell_check(splitted_texts): 
    spell_checked_lst = []
    for senten in splitted_texts:
        result = spell_checker.check(senten)
        result = result.as_dict()
        result = result['checked']
        if len(result) != 0:
            spell_checked_lst.append(result)
        else: 
            spell_checked_lst.append(senten)

        # print('origin: ', result['original'])
        # print('changed:',result['checked'])
        # print('--------------------------------')
    return spell_checked_lst

    ## 그래두, 아무말두와 같은 조사 "두"는 "도"로 잘 교정하지만, -허다, -말구 와 같은 사투리체는 변형하지 못함