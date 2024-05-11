import requests



url = "http://localhost:8000/actuaire/stream"


def getResponse(text):
    response = requests.post(url, json={"input": text})
    print(response)
    return response.json()['output']


input_text = "What are the registers of the 6510?"

response = getResponse(input_text) 
for chunk in response:
    print(chunk.decode())
