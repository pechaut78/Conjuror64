import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

import os

class VStore:
    def __init__(self, name,embed_model):
        self.name = name
        self.db = None
        print("Loading Embedding Model...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
        if os.path.exists(self.name):
            self.local_index=Chroma(persist_directory=self.name, embedding_function=self.embeddings)
        else:
           self.local_index = None  
   



    def addFile(self,fname):
        if fname.endswith('.txt'):
            self.addDocx(fname)
    
    def get_store(self):
        return self.local_index
    
    def addDocx(self,fname):
        print("Loading Doc...")
        with open(fname) as f:
          text = f.read()
        print("Splitting Doc...")        
        separator = "\n\n\n\n"
        _docs = text.split(separator)
        docs = [doc for doc in _docs if doc.strip() and len(doc.strip()) >= 3]
        print(f"Nombre de segments trouvés : {len(docs)}")     
        
        print("Indexing Doc...")
        

        if self.local_index is not None:
            self.db.add_documents(documents=docs)
        else:
            self.db = Chroma.from_texts(texts=docs, embedding=self.embeddings,persist_directory=self.name)

        docs = self.db.similarity_search("what are the registers of the 6510")
        print(docs)