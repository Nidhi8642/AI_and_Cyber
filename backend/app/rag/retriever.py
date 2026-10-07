from app.rag.ingest import load_documents

def search_knowledge_base(query: str, top_k: int = 3 ) -> list[dict]:
    documents = load_documents()
    query_words = set(
        query.lower().split()
    )

    scored_documents = []

    for document in documents:
        content = document["content"].lower()
        score = sum(
            1
            for word in query_words
            if word in content
        )
        if score > 0:
            scored_documents.append(
                {
                    "source" : document["source"],
                    "content" : document["content"],
                    "score" : score
                }
            )
    scored_documents.sort(
        key = lambda item: item["score"],
        reverse=True
    )

    return scored_documents[:top_k]