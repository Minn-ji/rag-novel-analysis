from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForCausalLM
from transformers import pipeline

class PersonNameRoBERTaRepository:
    __instance = None

    model = AutoModelForTokenClassification.from_pretrained("vitus9988/klue-roberta-small-ner-identified")
    tokenizer = AutoTokenizer.from_pretrained("vitus9988/klue-roberta-small-ner-identified")

    roberta_ner = pipeline("token-classification", model=model, tokenizer=tokenizer)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            return cls.__instance
    
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def extract_PS_token(self, splitted_texts):
        person_names = []
        for text in tqdm(splitted_texts, desc='get person name with RoBERTa'):
            tokens = self.roberta_ner(text)
            name = [] 

            for token in tokens:
                if token['entity'].startswith('B-PS'):  # B-PS : start of person name
                    if name: 
                        person_names.append(''.join(name).replace('#','')) 
                    name = [token['word']]  
                elif token['entity'].startswith('I-PS'):  # I-PS : part of person name
                    name.append(token['word'])

            if name:
                person_names.append(''.join(name).replace('#',''))
        
        return person_names