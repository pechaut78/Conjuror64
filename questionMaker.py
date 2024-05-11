from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain import PromptTemplate
from langchain.prompts.chat import  ChatPromptTemplate,HumanMessagePromptTemplate
from langchain.schema import  SystemMessage
import argparse
import os,re
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()
model = None


prompt = PromptTemplate(
    template="""you are training an LLM and generating a csv of questions and verbose answers just answer providing pairs no other text like:
    "question1","answer1"
    "question2","answer2"

    Important, do not numerorate the questions.
    only create  questions whose answer is in the text.
    provide 10 differentunique standalone short questions and long verbose answers about this text: <{text}>. IMPORTANT: only provide questions and answers pairs, no other sentence""",
    input_variables=["text"],
)

long_prompt = PromptTemplate(
    template="""you are training an LLM and generating a csv of questions and verbose answers just answer providing pairs no other text like:
    "question1","answer1"
    "question2","answer2"
    
    only create  questions whose answer is in the text.
    Important, do not numerorate the questions.
    provide 30 different unique standalone short questions and long verbose answers about this text: <{text}>. IMPORTANT: only provide questions and answers pairs, no other sentence""",
    input_variables=["text"],
)
chain = None
long_chain = None

def remove_before_first_quote(text):
    # Trouve l'index du premier guillemet
    first_quote_index = text.find('"')
    
    # Vérifie si un guillemet a été trouvé
    if first_quote_index != -1:
        return text[first_quote_index:]

def correct_line_breaks(text):
    # Remplace les sauts de ligne incorrects (sauf ceux après une guillemet fermante)
    corrected_text = re.sub(r'(?<=")\n\n(?=")', '\n', text)
    return corrected_text

def correct_internal_quotes(text):
    # Remplace les guillemets internes, en conservant ceux qui délimitent les éléments
    # Utilise une expression régulière pour détecter les guillemets non couplés correctement
    corrected_text = re.sub(r'(?<=[a-z0-9])"(?=[a-z0-9])', "'", text, flags=re.IGNORECASE)
    return corrected_text

def handleQA(fname,text):
    res = "question,answer\n"
    if len(text) < 2000:
        t= chain.invoke({"text": text})
    else:
        t = long_chain.invoke({"text": text})

    t = remove_before_first_quote(t)
    t = correct_line_breaks(t)
    t = correct_internal_quotes(t)
    print(t)
    csv_filename = f"{fname}.csv" 
    with open(csv_filename, 'w', encoding='utf-8') as file:
        file.write(res+t)


def main():
    parser = argparse.ArgumentParser(description="Process each .txt file in a given directory.")
    parser.add_argument("directory", type=str, help="The directory to process")
    args = parser.parse_args()

    directory = args.directory
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
    groq_model = os.getenv("GROK_MODEL")
    api_key = os.getenv("GROK_API_KEY")


    global model
    model = ChatGroq(groq_api_key=api_key,model_name=groq_model, temperature=0.0)
    print(model)
    global chain
    chain = prompt | model | output_parser
    global long_chain
    long_chain = long_prompt | model | output_parser

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            base_filename = os.path.splitext(filename)[0] 
            fname = os.path.join(directory, base_filename)
            handleQA(fname,text)
            print(f"Processed {filename}")
            



if __name__ == "__main__":
    main()