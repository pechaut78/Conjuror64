
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain import PromptTemplate
import argparse
import os,re
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()
model = None


prompt = PromptTemplate(
    template="""your goal is to create a question that would accept the following text as answer:
       <{text}>. IMPORTANT: only provide the question, no other sentence""",
    input_variables=["text"],
)

chain = None
long_chain = None

def handleQA(fname,text):
    text = text.strip().replace('"', "'")
    res = "question,answer\n"
    t= chain.invoke({"text": text})


    csv_filename = f"q-{fname}.csv" 
    with open(csv_filename, 'w', encoding='utf-8') as file:
        file.write(res+f'"{t}","' + text+'"')


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