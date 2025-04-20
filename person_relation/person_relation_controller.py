import os
import itertools

from person_relation.service.person_relation_service import PersonRelationService
from util.text_preprocessing import load_json_data, split_texts, save_dict_result


def get_faiss_index():
    __personRelationService = PersonRelationService.getInstance()
    __personRelationService.create_faiss_index('sangroksu_no_preprocessed.txt')


def extract_person_relation(extracted_name_path):
    names = load_json_data('results/person_name_result/person_40_roberta.json').get('names')
    pairs = list(itertools.combinations(names, 2))
    
    __personRelationService = PersonRelationService.getInstance()
    chain = __personRelationService.create_qa_chain()
    result_lst = []
    for (person1, person2) in pairs:
        user_send_message = f"{person1}과 {person2}은 소설에서 어떤 관계입니까?"
        done = False

        while not done:
            relation = __personRelationService.invoke_chain(chain, user_send_message)  # 예상 출력 예: "초반: ... 중반: ... 후반: ..."
            try:
                if '없음' in relation:
                    part1, part2, part3 = None, None, None
                else:
                    # 예상하는 형식인지 확인
                    if '초반:' in relation and '중반:' in relation and '후반:' in relation:
                        # "초반:" 키워드 바로 뒤부터 "중반:" 바로 앞까지
                        idx_start = relation.find('초반:') + len('초반:')
                        idx_mid = relation.find('중반:')
                        part1 = relation[idx_start:idx_mid].strip()

                        # "중반:" 바로 뒤부터 "후반:" 바로 앞까지
                        idx_mid_start = relation.find('중반:') + len('중반:')
                        idx_end = relation.find('후반:')
                        part2 = relation[idx_mid_start:idx_end].strip()

                        # "후반:" 바로 뒤부터 끝까지
                        idx_end_start = relation.find('후반:') + len('후반:')
                        part3 = relation[idx_end_start:].strip()
                    else:
                        # 예상 형식이 아닐 경우 에러 발생
                        raise ValueError("(초반:, 중반:, 후반:)을 찾을 수 없음")
                
                done = True  # 파싱 성공 시 반복문 종료

            except Exception as e:
                print("관계 정보 파싱 에러:", e)
        rel1 = {'node':person1, 'target':person2, 'edge':part1,'part':1}
        rel2 = {'node':person1, 'target':person2, 'edge':part2,'part':2}
        rel3 = {'node':person1, 'target':person2, 'edge':part3,'part':3}
        result_lst.append(rel1)
        result_lst.append(rel2)
        result_lst.append(rel3)
    
    os.makedirs('results/person_relation_result', exist_ok=True)
    file_name = f'results/person_relation_result/{extracted_name_path}.json'
    save_dict_result({'relations': result_lst}, file_name)

if __name__=='__main__':extracted_name_path
    # get_faiss_index()
    extract_person_relation('person_40_roberta')