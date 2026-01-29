import os
from dotenv import load_dotenv
from mistralai import Mistral
import time

import mistralai
load_dotenv()

client = Mistral(os.getenv('MISTRAL_API_KEY'))
model = "mistral-embed-2312"

def get_embeddings(texts: list[str]) -> list[list[float]]:
    time.sleep(2)
    answer_gotten = False
    max_retries = 4
    while not answer_gotten and max_retries > 0:
        try :
            embedding = client.embeddings.create(model=model,inputs=texts)
            answer_gotten = True
        except mistralai.SDKError as e:
            print(f"Erreur API Mistral : {e}")
            max_retries -= 1
            time.sleep(20)  # Attendre plus longtemps pour les erreurs serveur
    return [emdata.embedding for emdata in embedding.data]



if __name__ == "__main__":
    test = get_embeddings("Bonjour le monde")
    print(f"Dimension du vecteur : {len(test)}")
    print(f"Premiers éléments : {test[:5]}")