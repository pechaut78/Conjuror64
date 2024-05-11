import argparse
from classes.vstore import VStore
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
model_embedd = os.getenv("MODEL_EMBEDD")




def main():
    parser = argparse.ArgumentParser(description="Handle the VectoreStore")
    parser.add_argument('-s', '--store', type=str, help='store to use', default='kb_store')
    parser.add_argument('-a', '--add', type=str, help='file to add')

    args = parser.parse_args()

    fname =""
    if args.add:
        fname = args.add
    
    store=""
    if args.store:
        store = args.store
    
    if store == '':
        print("Error: store name cannot be empty, use -s")
        return

    vstore = VStore(store,model_embedd)
    vstore.addFile(fname)




if __name__ == '__main__':
    main()