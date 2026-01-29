import os
import time
import mistralai
from mistralai import Mistral
import json


api_key = os.environ["MISTRAL_API_KEY"]
model = "ministral-14b-latest"


client = Mistral(api_key=api_key)


def evaluate_answer(question: str, context: list[str], answer: str) -> dict:
    max_retries = 3
    correct_result = False
    context = "\n".join(context)
    messages = [
    {
    "role": "user",
    "content": f"""
    Question : {question}
    Contexte : {context}
    Réponse donnée : {answer}
    
    
    Évalue la réponse ci-dessus de manière concise et exigente. Répond avec un object JSON comme suit :  
    {{
        "fidelity": 12,
        "relevance": 11,
        "explanation": "..."
    }}
    
    fidelity : # La réponse est-elle fidèle au contexte ? note sur 20
    relevance : # La réponse répond-elle à la question ? note sur 20
    explanation : # Pourquoi ces notes ? Comment améliorer ? Doit inciter à répondre de manière concise.
    
    """,
    }
    ]
    while not correct_result and max_retries > 0:
        answered = False
        max_retries = 4
        while not answered and max_retries > 0:
            try :
                time.sleep(4)
                chat_response = client.chat.complete(
                    model = model,
                    messages = messages,
                    response_format = {
                        "type": "json_object",
                    }
                )
                answered = True
            except mistralai.SDKError as e:
                print(f"Erreur API Mistral : {e}")
                max_retries -= 1
                time.sleep(20)  # Attendre plus longtemps pour les erreurs serveur
        try :
            result = json.loads(chat_response.choices[0].message.content)
            if "fidelity" in result.keys() and "relevance" in result.keys() and "explanation" in result.keys():
                correct_result = True
            else:
                print("Réponse invalide, réessai...")
                time.sleep(1)
                max_retries -= 1
        except json.JSONDecodeError as e:
            print(f"JSON invalide : {e}")
            max_retries -= 1
            time.sleep(2)
        except mistralai.SDKError as e:
            print(f"Erreur API Mistral : {e}")
            max_retries -= 1
            time.sleep(20)  # Attendre plus longtemps pour les erreurs serveur
            
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            max_retries -= 1
            time.sleep(2)
    if not correct_result:
        return {
        "fidelity": 0,
        "relevance": 0,
        "explanation": "Évaluation échouée après 3 tentatives"
        }
    return result