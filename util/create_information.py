import os
import chardet

from util.text_preprocessing import detect_encoding

def count_file_stats(file_path):
    encoding = detect_encoding(f'data/{file_path}')
    print('file encoded with', encoding)
    with open(f'data/{file_path}', "r", encoding=encoding) as file:
        content = file.read()

    byte_size = len(content.encode("cp949", errors="ignore"))
    char_count = len(content)
    word_count = len(content.split())
    line_count = content.count("\n") + 1

    stats = (
        f"파일명: {file_path}\n"
        f"바이트 수: {byte_size}\n"
        f"문자 수: {char_count}\n"
        f"단어 수: {word_count}\n"
        f"라인 수: {line_count}\n"
    )
    os.makedirs('results/info_result', exist_ok=True)
    
    with open(f"results/info_result/READM_for_{file_path[:-4]}.txt", "w",encoding="cp949") as output_file:
        output_file.write(stats)

    print("파일 분석 완료")
    print(stats)

if __name__ == '__main__':
    count_file_stats("상록수_심대섭.txt")