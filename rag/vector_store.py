from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from google import genai
import os


class GeminiEmbeddings(Embeddings):
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def embed_documents(self, texts):
        embeddings = []

        for text in texts:
            response = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=text,
            )

            embeddings.append(response.embeddings[0].values)

        return embeddings

    def embed_query(self, text):
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        return response.embeddings[0].values


def create_vector_store(chunks):
    embedding_model = GeminiEmbeddings()

    vector_db = FAISS.from_texts(
        texts=chunks,
        embedding=embedding_model,
    )

    return vector_db