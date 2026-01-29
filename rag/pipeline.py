import rag.retriever as retriever
import rag.generator as generator
import rag.judge as judge
import time

def ask(question: str, max_attempts: int = 2, early_stopping: bool = True) -> dict:
    # 1 Récupérer les chunks pertinents
    context = retriever.search(question, n_results=2)
    # 2 Générer une réponse
    time.sleep(1)
    answer = generator.generate_answer(question, context)
    n_attempts = 1
    # 3 Evaluer la réponse
    time.sleep(1)
    evaluation = judge.evaluate_answer(question, context, answer)

    # debug : afficher reponse et evaluation
    # print(f"Réponse : {answer}")
    # print(f"Evaluation : {evaluation}")

    # 4 Si la réponse est inexacte, réessayer jusqu'à max_attempts
    if early_stopping :
        while n_attempts < max_attempts and evaluation["fidelity"] < 15 or evaluation["relevance"] < 15:
            
            # debug afficher note insuffisante
            # print(f"Note insuffisante : {evaluation['fidelity']}, {evaluation['relevance']}")
            context = retriever.search(question, n_results=2+n_attempts)
            time.sleep(1)
            answer = generator.generate_answer_retry(question, answer, evaluation["explanation"], context)
            time.sleep(1)
            evaluation = judge.evaluate_answer(question, context, answer)
            time.sleep(1)
            n_attempts += 1
    else:
        while n_attempts < max_attempts and evaluation["fidelity"] < 20 or evaluation["relevance"] < 20:
            # debug afficher note insuffisante
            # print(f"Note insuffisante : {evaluation['fidelity']}, {evaluation['relevance']}")
            context = retriever.search(question, n_results=2+n_attempts)
            time.sleep(1)
            answer = generator.generate_answer_retry(question, answer, evaluation["explanation"], context)
            time.sleep(1)
            evaluation = judge.evaluate_answer(question, context, answer)
            time.sleep(1)
            n_attempts += 1
    # 5 retourner la réponse finale
    dictAnswer = {
        "answer": answer,
        "evaluation": evaluation,
        "attempts": n_attempts,
    }

    return dictAnswer