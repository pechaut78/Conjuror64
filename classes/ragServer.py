import os
from classes.vstore import VStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import MessagesPlaceholder,PromptTemplate
from langchain.memory import ChatMessageHistory
from operator import itemgetter
from langchain.chains import create_history_aware_retriever
from langchain import hub
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableBranch
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.memory import ConversationBufferMemory



import re

class ragServer:
    def __init__(self,store_name,embed_model,system_prompt,user_prompt,formatted_prompt=""):
        self.store = VStore(store_name,embed_model)
        if self.store.local_index == None:
            print("Error: store not found")
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.chain =None
        self.chat_history = []
        self.formatted_prompt = formatted_prompt
        
    

    def createChain(self,model_type,model_key,model_name,groq_model=""):
        
        self.model_name = model_name
        self.model_key = model_key

        print(model_name)

        if(model_type=="lmstudio"):
            self.model = ChatOpenAI(base_url="http://localhost:1234/v1",temperature=0.9,model=model_name,api_key=model_key)
        elif model_type=="ollama":
            self.model= Ollama(model=model_name)
        elif model_type=="groq":
            self.model = ChatGroq(groq_api_key=model_key,model_name=groq_model)
        else:self.model = ChatOpenAI(temperature=0.9,model=self.model_name,api_key=self.model_key,streaming=True)


        retriever = self.store.get_store().as_retriever(search_type="mmr", search_kwargs={"k": 3,"score_threshold": 0.5})

        def print_value(x):
            print(x)
            return x

        def cleanSimilarities(sims):
            cleaned_text ="context:["
            for elem in sims:
                cleaned_text += "\n"+ elem.page_content.replace("\\n"," ").replace("\\xa0"," ").strip()
                cleaned_text =  re.sub(r'\n+', '\n', cleaned_text)
            cleaned_text += "]"

            return cleaned_text


        self.prompt = ChatPromptTemplate.from_messages(
            [("system",self.system_prompt+" {context}"),
             ("user", self.user_prompt+" {question}"),
             
             ])
        
        self.chain = (
            {"context": retriever| cleanSimilarities,"question": RunnablePassthrough()}
            | self.prompt
            | self.model
            | StrOutputParser()
            
        )


        
        self.prompt_history = ChatPromptTemplate.from_messages(
            [("system",self.system_prompt+" {context}"),
              MessagesPlaceholder(variable_name="history"),
             ("user", self.user_prompt+" {input}"),             
             ])
        self.prompt_condensed = ChatPromptTemplate.from_messages(
            [("system",self.system_prompt+" {context}"),
             ("user", self.user_prompt+" {rephrased_input}"),             
             ])

        from langchain_core.runnables.history import RunnableWithMessageHistory

        #rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")



        condense_question_template = """
            Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. Answer in the same language as the followup question. Only provide the question.
    
            Chat History: {history}
            Follow Up Question: {input}
            Standalone question:
        """
        condense_question_prompt = PromptTemplate.from_template(condense_question_template)

        self.chat_rephrase_chain = RunnableBranch(
            (lambda x: not x.get("history", False),
             lambda x: x["input"]) ,
            condense_question_prompt | self.model | StrOutputParser()
        ).with_config(run_name="chat_rephrase_chain")

        
       
        self.chat_retriever_chain = (
             {"input": lambda x: x.get("rephrased_input","Hello")} | retriever
        )
        #self.chat_retriever_chain = create_history_aware_retriever(self.model, self.store.as_retriever(), condense_question_prompt)
        
        def format_docs(d):
            l = d.get("input","Hello")
            print(l)
            return l
        
        self.chain_with_chat_history = (
            {"input": itemgetter("input"), "history": itemgetter("history")}
            | self.chat_rephrase_chain
            | (lambda x: {"rephrased_input": x})
            | {"input": itemgetter("rephrased_input")}
            | {"context": format_docs | retriever,"rephrased_input": itemgetter("input")}
            | self.prompt_condensed
            | self.model
            | StrOutputParser()   
        )


        #self.chain_with_chat_history = (
        #    {"context": self.chat_retriever_chain,"input": itemgetter("input"),"chat_history": itemgetter("chat_history") }
        #    | self.prompt_history
        #   | self.model
        #    | StrOutputParser()   
        #)

        chat_history_for_chain = ChatMessageHistory()
         

        self.chain_with_message_history = RunnableWithMessageHistory(
          self.chain_with_chat_history,
          lambda session_id: chat_history_for_chain,
            input_messages_key="input",
            history_messages_key="history",
        )

       
        

    
        self.fprompt = ChatPromptTemplate.from_messages(
            [("system",self.formatted_prompt),
             ("user", self.user_prompt+" {input}"),
             
             ])
        
        self.formatted_chain = (
            self.chain_with_chat_history
            | self.fprompt
            | self.model
            | StrOutputParser()
        )

    def getChainWithFormat(self):
        return self.formatted_chain
      
    def getChaniWithMessageHistory(self):
        if self.chain_with_message_history is None:
            print("Chain not created")
            return None
        return self.chain_with_message_history
    
    def getChain(self):
        if self.chain is None:
            print("Chain not created")
            return None
        return self.chain

    def invoke_mem(self, text):
        print(self.chain.invoke(
            {"ability": "math","question": "What does cosine mean?","chat_history":"[]"},
            config={
                "configurable": {"user_id": "user_id","conversation_id": "conversation_id"}
            },


        ))