import json

from app.clients.groq import GroqClient
from app.db import query
from app.settings import MODEL_NAME, N_RESULTS, THRESHOLD

groq = GroqClient(model=MODEL_NAME)

def _prepare_context(query_result, question):
    content = [
        {
            "id": match["id"],
            "title": match["metadata"]["name"],
            "url": match["metadata"]["url"],
            "content": match["content"],
        }
        for match in query_result
    ]

    context = {
        "content": content,
        "question": question,
    }
    
    return context

def _format_response(query_result, prediction):
    if prediction is None:
        structured_prediction = {
            "answer": "I do not know the answer to the question.",
            "source_ids": []
        }
    else:
        structured_prediction = json.loads(prediction)
        
    response = {
        "answer": structured_prediction["answer"],
        "sources": [],
    }

    for source_id in structured_prediction["source_ids"]:
        match = None
        for r in query_result:
            if r["id"] == source_id:
                match = r
                break

        if match is not None:
            response["sources"].append({
                "id": source_id,
                "title": match["metadata"]["name"],
                "url": match["metadata"]["url"],
            })

    if not response["sources"]:
        response["answer"] = "I do not know the answer to the question."

    return response

def answer_question(question):
    try:
        query_result = query(question, n_results=N_RESULTS, threshold=THRESHOLD)

        context = _prepare_context(query_result, question)

        prediction = groq.predict(context=context)

        response = _format_response(query_result, prediction)

        return response
    except Exception:
        return {"error": "An error occurred"}
