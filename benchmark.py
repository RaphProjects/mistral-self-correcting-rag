from rag.pipeline import ask
from rag.retriever import index_documents
from rag.document_loader import load_pdf
import json
import time

print("Indexation des documents...")
docs = load_pdf(["pdfs/cryptage2048.pdf", "pdfs/xyz42.pdf"])
index_documents(docs)
print("Indexation terminée !")

questionsCR2048 = [
    "Quel organisme a émis le document technique confidentiel du SCA-2048 ?",
    "En réponse à quelles menaces croissantes ce système de cryptage a-t-il été développé ?",
    "Quel est le nom du projet financé par le programme Horizon Europe qui a initié ce protocole ?",
    "Quelles institutions de Munich, Lausanne et Lyon ont collaboré au développement ?",
    "Quelle est la valeur de la protection estimée contre les attaques quantiques de type Shor ?",
    "Quel est l'algorithme de base utilisé, spécifié comme une variante du CECA-K ?",
    "Quelle fonction de hachage est employée avec un salage dynamique ?",
    "Quel est le polynôme irréductible utilisé sur le corps fini GF(2^2048) ?",
    "Quelle est l'équation de la courbe elliptique auxiliaire EC-AUX-2048 ?",
    "Quelle est la valeur de la constante d'initialisation CI-Alpha (tronquée) ?",
    "Quelle version du protocole a corrigé la vulnérabilité oracle CVE-2023-SCA-0041 ?",
    "Depuis quelle date le Groupement Bancaire Européen utilise-t-il ce système pour les transactions SEPA ?",
    "Quelle désignation l'Agence Européenne de Défense utilise-t-elle pour ce protocole ?",
    "Quel projet pilote de chiffrement de dossiers médicaux a débuté en janvier 2024 ?",
    "Quelles sont les bibliothèques de langages disponibles pour l'implémentation du SCA-2048 ?",
    "Quelle réduction de consommation énergétique le SCA-2048 offre-t-il par rapport au RSA-4096 ?",
    "Quel type d'instructions processeur est nécessaire pour des performances optimales ?",
    "Quelle est la taille des signatures générées par le SCA-2048 ?",
    "Quel est le nom du programme de formation nécessaire pour l'implémentation correcte ?",
    "Quel module de révocation dynamique est prévu pour la version 4.0.0 en 2025 ?"
]

questionsXYZ42 = [ 
    "Quel est l'objectif principal du protocole XYZ-42 ?",
    "Où le développement du protocole XYZ-42 a-t-il commencé ?",
    "Qui est la directrice de l'équipe ayant développé ce protocole ?",
    "En quelle année les tests du protocole ont-ils été réussis ?",
    "Quand le protocole a-t-il été officiellement adopté par des organisations internationales ?",
    "Quelle est la fréquence de fonctionnement du protocole XYZ-42 ?",
    "Quel est le taux de transmission de données mentionné dans le document ?",
    "Quelle distance maximale la communication peut-elle atteindre ?",
    "Quel est le taux d'erreur du protocole ?", 
    "Quels éléments physiques sont utilisés pour transmettre les informations ?",
    "Comment le protocole garantit-il la détection immédiate d'une interception ?", 
    "Quelle technique est utilisée pour assurer l'intégrité des données ?",
    "Quels matériaux spécifiques sont requis pour une implémentation optimale ?", 
    "À quelle température les composants doivent-ils être maintenus ?", 
    "Comment les photons intriqués sont-ils générés en laboratoire ?", 
    "Quel support est utilisé pour la transmission des photons ?", 
    "Quelle technologie les récepteurs utilisent-ils pour lire les états quantiques ?", 
    "Quel a été le rôle de la ville de Paris dans le déploiement de 2024 ?", 
    "Quelle réduction des tentatives d'interception l'OTAN a-t-elle constatée en 2025 ?", 
    "Quels composants sont refroidis pour minimiser les interférences ?" ]

max_attempts_bench = 5

n_questions_bench = 10


performances = {} # dictionnaire de dictionnaires de dictionnaires : performance[question][i_attempts]["fidelity/relevance"]
for question in questionsXYZ42[:n_questions_bench]+questionsCR2048[:n_questions_bench]:
    performances[question] = {}
    print(f"Test de la question : \"{question}\" \n En cours...")
    for i in range(1,max_attempts_bench+1):
        time.sleep(2) # léger delay supplémentaire pour ne pas dépasser les limites de l'API
        result = ask(question, max_attempts=i,early_stopping=False)
        relevance = result["evaluation"]["relevance"]
        fidelity = result["evaluation"]["fidelity"]
        performances[question][f"{i}_attempts"] = {"fidelity":fidelity,"relevance":relevance}

        # sauvegarde progressive 

        with open("benchmark_results.json", "w") as f:
            json.dump(performances, f, indent=2)

print("Benchmark terminé ! Voir benchmark_results.json pour les résultats.")
 