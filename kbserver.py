import os
from dotenv import load_dotenv
from classes.ragServer import ragServer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
import uvicorn



import argparse




def main():

    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
    store_name = os.getenv("VSTORE_NAME")
    model_embedd = os.getenv("MODEL_EMBEDD")
    api_key = os.getenv("OPENAI_API_KEY")
    model_type = os.getenv("MODEL_TYPE") 
    model_name = os.getenv("MODEL_NAME")
    actuaire_port = os.getenv("ACTUAIRE_PORT")
    if(model_type=="groq"):
        groq_model = os.getenv("GROK_MODEL")
        api_key = os.getenv("GROK_API_KEY")

    print("Model Type:",model_type,"Model Name:",model_name)
    parser = argparse.ArgumentParser(description="Handle the KnowledgeServer")
    parser.add_argument('-s', '--store', type=str, help='store to use', default=store_name)


    args = parser.parse_args()
    store_name = args.store

 #   system_prompt = "Tu es un professeur, Réponds à la question en français et en t'inspirant  des éléments suivants et en paraphrasant, sans mentionner que tu utilises un document, soit précis:"
    system_prompt = """Tu es Sam, un professeur d'actuariat et tu réponds en français. Réponds en paraphrasant uniquement les informations pertinentes sans jamais mentionner ni suggérer que la réponse provient d'un texte, d'un document ou que tu utilises une source externe. Commence ta réponse directement par les faits ou par une affirmation, comme si tu répondais à partir de ta propre expertise. 

Informations disponibles :
    """
 
    user_prompt= " "
   # slide_prompt= """ Créé un titre à partir de la demande de l'utilisateur, un résumé en une ligne très courte de la demande, et enfin recopie la demande de l'utilisateur. Lorsque tu réponds, utilise uniquement le format structuré spécifié ci-dessous sans aucune introduction ou texte supplémentaire. Réponds directement avec le format suivant :
#
 #   "title": "<titre dans la même langue que la demande>"
  #  ,
 #   "summary": "<résumé court dans la même lanque que la demande>"
 #   ,
 #   "content": "<contenu détaillé de la demande de l'utilisateur>"
#
#     """
    slide_prompt= """ Crée un titre et un résumé en une ligne très courte basés sur la demande de l'utilisateur. Puis, recopie exactement et intégralement la demande de l'utilisateur sans ajouter, omettre, ou modifier aucun mot.
    Pour summary, identifie le mot le plus important qui capture le sens de la demande et entoure ce mot avec des balises HTML <em>  pour le mettre en évidence.
    Utilise uniquement le format structuré spécifié ci-dessous sans aucune introduction ou texte supplémentaire. Réponds directement avec le format suivant :

"title": "<titre basé sur la demande, dans la même langue que la demande>"
,
"summary": "<résumé court et concis de la demande, dans la même langue que la demande>"
,
"content": "<copie intégrale et exacte de la demande de l'utilisateur>

"""
    
    rag = ragServer(store_name,model_embedd,system_prompt,user_prompt,slide_prompt)
    rag.createChain(model_type,api_key,model_name,groq_model)

    app = FastAPI(
        title="Kb Teacher",
        version="1.0",
        description="Ask your teacher",
    )

    app.add_middleware(
    CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )   

    add_routes(
        app,
        rag.getChain(),
        path="/actuaire",
        playground_type="chat"
    )


    add_routes(
        app,
        rag.getChaniWithMessageHistory(),
        path="/actuaire_mem",
        playground_type="chat"
    )

    add_routes(
        app,
        rag.getChainWithFormat(),
        path="/actuaire_slides",
        playground_type="chat"
    )

    # _str = rag.getChaniWithMessageHistory().invoke(
    #     { "input": "What does cosine mean?"},
    #     config={
    #         "configurable": {"session_id": "session_id","user_id": "user_id","conversation_id": "conversation_id"}
    #     },
    # )
    # print(_str)
    uvicorn.run(app, host="localhost", port=int(actuaire_port))


if __name__ == '__main__':
    print("Starting Server...")
    main()
    