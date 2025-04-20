ㅣfrom langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory


class PersonRelationRAGRepository:
    __instance = None
    store = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            return cls.__instance
    
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    def generate_prompt(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                        """당신은 소설 『상록수』 전문 분석가입니다. 다음 규칙을 엄격히 지켜주세요:
                            1. 제공된 소설 내용에서만 정보를 활용할 것
                            2. 등장인물 관계는 반드시 원문의 서술에 근거할 것
                            3. 추측이나 일반 상식을 사용하지 말 것
                            4. 출력은 두 사람의 관계를 시점에 따라 총 세 번 제시하며, "초반: 중반: 후반: " 형식으로 제시할 것
                            5. 각 관계의 종결 어미는 '함', '음' 등으로 끝낼 것.
                            6. 단, 제시된 두 사람 사이에 접점이 없을 시 '없음'이라는 두 글자만 출력할 것"""
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human",         
                    """소설 내용: {context}
                        
                       질문: {question}"""),
            ]
        )
        return prompt


    def load_LLMChain(self):
        return ChatOpenAI(model="gpt-4o-mini")


    def get_session_history(self, session_ids='always_same'):
        if session_ids not in self.store:
            self.store[session_ids] = ChatMessageHistory()
        
        return self.store[session_ids]
