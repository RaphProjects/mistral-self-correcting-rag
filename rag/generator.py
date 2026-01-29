from mistralai import Mistral
import os
import time

import mistralai

model = "ministral-14b-latest"

client = Mistral(os.getenv('MISTRAL_API_KEY'))

def generate_answer(question: str, context: list[str]) -> str:
    # Formater le contexte

    formated_context = ""

    for chunk in context:
        formated_context += f"{chunk}\n"

    # Construire le prompt
    prompt = [

        {"role": "system", "content": f"""Tu es un assistant qui répond aux questions en utiisant le contexte fourni de manière concise. Si la réponse ne se situe
         pas dans le contexte, dis le clairement mais tente tout de même de répondre à la question.
         
         Context: {formated_context}"""},

        {"role": "user", "content": f"Question: {question}"},

    ]

    max_retries = 4
    answer_gotten = False
    time.sleep(2)
    while not answer_gotten and max_retries > 0:
        try :
            answer = client.chat.complete(model=model,messages=prompt)
            answer_gotten = True
        except mistralai.SDKError as e:
            print(f"Erreur API Mistral : {e}")
            max_retries -= 1
            time.sleep(20)  # Attendre plus longtemps pour les erreurs serveur
    return answer.choices[0].message.content

def generate_answer_retry(question: str, reponse_fausse: str, explanation: str, context: list[str]) -> str:
    # Formater le contexte

    formated_context = ""

    for chunk in context:
        formated_context += f"{chunk}\n"

    # Construire le prompt
    prompt = [

        {"role": "system", "content": f"""Tu es un assistant qui répond aux questions de manière concise en utiisant le contexte fourni. Si la réponse ne se situe
         pas dans le contexte, dis le clairement mais tente tout de même de répondre à la question.
         
         Context: {formated_context}"""},

        {"role": "user", "content": f"Question: {question}"},

        {"role": "system", "content": f"""Un autre assistant a répondu à la question avec la réponse suivante : {reponse_fausse}.
         Cette réponse a été jugée non optimale pour les raisons suivantes : {explanation}.

         Tu dois répond à la question {question} de manière concise sans commettre les mêmes erreurs que l'assistant précédent, sans faire mention 
         de sa tentative. Tu dois répondre en utilisant le contexte fourni.
         
         """},

    ]
    # Appeler l'API mistral pour obtenir une réponse
    time.sleep(3)
    answer_gotten = False
    max_retries = 4
    while not answer_gotten and max_retries > 0:
        try :
            answer = client.chat.complete(model=model,messages=prompt)
            answer_gotten = True
        except mistralai.SDKError as e:
            print(f"Erreur API Mistral : {e}")
            max_retries -= 1
            time.sleep(20)  # Attendre plus longtemps pour les erreurs serveur


    return answer.choices[0].message.content