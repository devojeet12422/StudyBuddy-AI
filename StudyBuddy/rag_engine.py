import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGEngine:

    def __init__(self, chunk_size=1200, chunk_overlap=200):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.chunks = []
        self.vectorizer = None
        self.matrix = None


    def create_chunks(self, pages):

        chunks = []

        for page_number, page_text in pages:

            text = re.sub(
                r"\s+",
                " ",
                page_text
            ).strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = start + self.chunk_size

                chunk_text = text[start:end]

                if chunk_text.strip():

                    chunks.append(
                        {
                            "text": chunk_text,
                            "page": page_number
                        }
                    )

                start += (
                    self.chunk_size
                    - self.chunk_overlap
                )

        return chunks


    def build_index(self, pages):

        self.chunks = self.create_chunks(
            pages
        )

        if not self.chunks:
            return

        texts = [
            chunk["text"]
            for chunk in self.chunks
        ]

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.matrix = (
            self.vectorizer.fit_transform(
                texts
            )
        )


    def retrieve(
        self,
        question,
        top_k=5
    ):

        if not self.chunks:
            return []

        question_vector = (
            self.vectorizer.transform(
                [question]
            )
        )

        similarities = cosine_similarity(
            question_vector,
            self.matrix
        )[0]

        ranked_indices = (
            similarities.argsort()[::-1]
        )

        results = []

        for index in ranked_indices[:top_k]:

            score = similarities[index]

            if score <= 0:
                continue

            results.append(
                {
                    "text": self.chunks[index]["text"],
                    "page": self.chunks[index]["page"],
                    "score": float(score)
                }
            )

        return results