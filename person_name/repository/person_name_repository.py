import os
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
from wordcloud import WordCloud
from collections import defaultdict
from util.text_preprocessing import save_dict_result

class PersonNameRepository:
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


    def normalize_name(self, name):
        suffixes = {'이', '아', '야', '님', '씨'}
        while len(name) > 1 and name[-1] in suffixes:
            name = name[:-1]
        
        if len(name) >= 3:
            sung = ['김','이','박','최','정','강', '황','윤','구','조','주',
                    '장','백','유','오','손','마','양', '고','배','권','도', '서']
            name = name[1:] if name[0] in sung else name[-2:]
        return name

    def get_name_map(self, extracted_names):
        normalized_map = defaultdict(list)
        for name in tqdm(extracted_names, desc='extract real name'):
            key = self.normalize_name(name.strip())
            normalized_map[key].append(name)
        
        return normalized_map

    def filter_n_names(self, normalized_map, n):
        filtered_names = [
            (key, len(count)) for key, count in normalized_map.items() 
            if len(count) >= n and len(key) in {2, 3}
        ]
        filtered_names = dict(filtered_names)

        return filtered_names


    def generate_wordcloud(self, freq, image_name='wordcloud_result'):
        cloud = WordCloud(font_path = 'data/NanumSquareR.ttf', 
                        background_color='white',
                        width=500, height=500)
        freq_cloud = cloud.generate_from_frequencies(freq)
        arr = freq_cloud.to_array()

        os.makedirs('results/person_wordcloud', exist_ok=True)
        fig = plt.figure(figsize=(5, 5))
        plt.imshow(arr)
        plt.show()
        fig.savefig(f'results/person_wordcloud/{image_name}.png')
        
        print('Saved in results/person_wordcloud/.')


    def save_name_result(self, filtered_names, n, roberta=True):
        os.makedirs('results/person_name_result', exist_ok=True)
        if roberta:
            file_name = f'person_{n}_roberta'
        else:
            file_name = f'person_{n}_kkam'

        file_name = f'results/person_name_result/{file_name}.json'
        
        save_dict_result({'names': filtered_names}, file_name)
        
