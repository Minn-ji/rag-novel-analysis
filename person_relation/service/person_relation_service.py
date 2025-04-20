import os
from dotenv import load_dotenv
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from person_relation.repository.person_relation_faiss_repository import PersonRelationFaissRepository
from person_relation.repository.person_relation_rag_repository import PersonRelationRAGRepository

load_dotenv()
openaiApiKey = os.getenv('OPENAI_API_KEY')
if not openaiApiKey:
    raise ValueError('API Key가 준비되어 있지 않습니다!')


class PersonRelationService:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__personRelationFaissRepository = PersonRelationFaissRepository.getInstance()
            cls.__instance.__personRelationRAGRepository = PersonRelationRAGRepository.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance
    
    def create_faiss_index(self, document):
        chunked_document = self.__personRelationFaissRepository.chunk_document(document)
        self.__personRelationFaissRepository.create_FaissIndex(chunked_document)
    

    def create_qa_chain(self):
        try:
            faiss_index = self.__personRelationFaissRepository.load_FaissIndex()

            chain = (
                    {
                        "context": itemgetter("question") | faiss_index.as_retriever(),
                        "question": itemgetter("question"),
                        "chat_history": itemgetter("chat_history"),
                    }
                    | self.__personRelationRAGRepository.generate_prompt()
                    | self.__personRelationRAGRepository.load_LLMChain()
                    | StrOutputParser()
            )

            qa_chain = RunnableWithMessageHistory(
                chain,
                self.__personRelationRAGRepository.get_session_history,
                input_messages_key="question", 
                history_messages_key="chat_history",
            )
            return qa_chain

        except Exception as e:
            print(e)
            print('-----------------------------\n## Create faiss index with your document at first.\n-----------------------------')


    def invoke_chain(self, chain, user_send_message):
        result = chain.invoke({"question": user_send_message},
                              config={"configurable": {"session_id": "always_same"}})
        return result