from tqdm import tqdm
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_experimental.text_splitter import SemanticChunker


class PersonRelationFaissRepository:
    __instance = None
    FAISS_INDEX_PATH = "assets/faiss_index_file"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            return cls.__instance
    
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    def chunk_document(self, document):
        # document = load_data(file_path)
        text_splitter = SemanticChunker(OpenAIEmbeddings())
        documents = text_splitter.create_documents([document])

        result = []
        for i, docu in tqdm(enumerate(documents), desc='chunking'):
            chk = f"chunk_{i+1}: {docu.page_content}"
            result.append(chk)
        return result


    def create_FaissIndex(self, chunked_document):
        embedding = OpenAIEmbeddings()
        faissIndex = FAISS.from_texts(texts=chunked_document, embedding=embedding)
        
        os.makedirs('assets', exist_ok=True)
        faissIndex.save_local(self.FAISS_INDEX_PATH)
        print('completed.')


    def load_FaissIndex(self):
        embeddings = OpenAIEmbeddings()
        faissIndex = FAISS.load_local(folder_path=self.FAISS_INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)
        return faissIndex