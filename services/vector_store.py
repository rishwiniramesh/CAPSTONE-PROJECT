import chromadb


class VectorStore:
    """
    Stores project knowledge in ChromaDB.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="database/chroma"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="project_knowledge"
            )
        )

    def clear(self):
        """
        Remove all previously stored project chunks.
        """

        count = self.collection.count()

        if count == 0:
            return

        ids = self.collection.get()["ids"]

        if ids:
            self.collection.delete(ids=ids)

    def add_documents(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        ids: list[str],
        metadatas: list[dict],
    ) -> None:

        self.collection.upsert(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ):

        count = self.collection.count()

        if count == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count),
        )

        return results