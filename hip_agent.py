import openai
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tiktoken
import re


class HIPAgent:
    def __init__(self):
        # Load OpenAI API key
        with open('openaikey.txt') as f:
            content = f.read().strip()
            openai.api_key = content.split(
                '=')[1] if '=' in content else content

        # Load and preprocess the textbook
        with open('textbook.txt', 'r') as f:
            self.textbook = f.read()
        self.textbook_chunks = self.chunk_text(self.textbook)

        # Create TF-IDF embeddings for textbook chunks
        self.tfidf = TfidfVectorizer()
        self.textbook_embeddings = self.tfidf.fit_transform(
            self.textbook_chunks)

    def get_embedding(self, text, model="text-embedding-ada-002"):
        """Get OpenAI embedding for a given text."""
        text = text.replace("\n", " ")
        response = openai.Embedding.create(input=[text], model=model)
        return response['data'][0]['embedding']

    def chunk_text(self, text, chunk_size=500, overlap=50):
        """Split text into overlapping chunks."""
        tokens = tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)
        chunks = []
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk = tokens[i:i + chunk_size]
            chunks.append(tiktoken.encoding_for_model(
                "gpt-3.5-turbo").decode(chunk))
        return chunks

    def retrieve_relevant_context(self, query, top_k=3):
        """Retrieve most relevant textbook chunks for a given query."""
        query_embedding = self.tfidf.transform([query])
        similarities = cosine_similarity(
            query_embedding, self.textbook_embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.textbook_chunks[i] for i in top_indices]

    def get_response(self, question, answer_choices, index):
        """Generate a response for a multiple-choice question."""
        # Retrieve relevant context from the textbook
        relevant_context = self.retrieve_relevant_context(question)
        context_str = "\n".join(relevant_context)

        # Create the prompt with question, choices, and context
        answer_str = "\n".join(
            f"{chr(65 + i)}. {choice}" for i, choice in enumerate(answer_choices))
        prompt = f"""Question: {question}\n\nChoices:\n{answer_str}\n\nAdditional Information:\n{context_str}\n\nThe correct answer is:"""
        print(f"----------------------- {index} ------------------------")
        # print(prompt)

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that solves multiple-choice questions using step-by-step reasoning."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000
        )
        full_response = response.choices[0].message.content
        print("Full response:\n" + full_response)

        # Extract the final answer and explanation
        # The explanation is for frontend display
        final_answer = re.search(r'([A-D])\.(.+?)(?=\n|$)', full_response)
        final_answer = final_answer.group(
            2).strip() if final_answer else full_response
        explanation = full_response.split(
            "Explanation:", 1)[-1].strip() if "Explanation:" in full_response else full_response

        print("Extracted final answer: " + final_answer)

        # Calculate cosine similarity between response and answer choices
        response_embedding = self.get_embedding(final_answer)
        choice_embeddings = [self.get_embedding(
            choice) for choice in answer_choices]
        similarities = [1 - cosine(response_embedding, choice_embedding)
                        for choice_embedding in choice_embeddings]

        # Return the index of the most similar answer choice and the explanation
        return np.argmax(similarities), explanation
