import json

from app.clients.groq import GroqClient
from app.db import query
from app.settings import MODEL_NAME, N_RESULTS, THRESHOLD


class Pipeline:
    def __init__(self):
        self.groq_client = GroqClient(model=MODEL_NAME)

    def _query(self, question):
        query_result = query(question, n_results=N_RESULTS)

        return query_result

    def _aggregate(self, query_result, threshold):
        count = len(query_result["ids"][0])

        formatted_result = []

        for match_index in range(count):
            id = query_result["ids"][0][match_index]
            document = query_result["documents"][0][match_index] # type: ignore
            metadata = query_result["metadatas"][0][match_index] # type: ignore
            distance = query_result["distances"][0][match_index] # type: ignore

            if distance < threshold:
                formatted_result.append({
                    "id": id,
                    "content": document,
                    "metadata": metadata,
                })

        return formatted_result

    def _prepare_context(self, aggregated_result, question):
        content = [
            {
                "id": match["id"],
                "title": match["metadata"]["name"],
                "url": match["metadata"]["url"],
                "content": match["content"],
            }
            for match in aggregated_result
        ]

        context = {
            "content": content,
            "question": question,
        }
        
        return context
    
    def _predict(self, context):
        prediction = self.groq_client.predict(context=context)

        return prediction

    def _validate_and_format_response(self, aggregated_result, prediction):
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

        titles = set()

        for source_id in structured_prediction["source_ids"]:
            match = None
            for result in aggregated_result:
                if result["id"] == source_id:
                    match = result
                    break

            # If the source is not in the query result, skip it as it is not a valid source
            # If the source is already in the response, skip it as we only want to include it once
            if match is not None and match["metadata"]["name"] not in titles:
                titles.add(match["metadata"]["name"])
                response["sources"].append({
                    "id": source_id,
                    "title": match["metadata"]["name"],
                    "url": match["metadata"]["url"],
                })

        if not response["sources"]:
            response["answer"] = "I do not know the answer to the question."

        return response

    def answer_question(self, question):
        try:
            query_result = self._query(question)
            aggregated_result = self._aggregate(query_result, threshold=THRESHOLD)
            context = self._prepare_context(aggregated_result, question)
            prediction = self._predict(context)
            response = self._validate_and_format_response(aggregated_result, prediction)

            return response
        except Exception:
            return {"error": "An error occurred"}


qa_pipeline = Pipeline()
