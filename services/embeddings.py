from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Converts project text into vector embeddings.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            [text],
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embedding[0].tolist()