import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Documents — ye tumhara "knowledge base" hai
documents = [
    "Python ek programming language hai jo 1991 mein Guido van Rossum ne banaya.",
    "AI agents autonomous systems hain jo khud decisions lete hain.",
    "LangChain ek framework hai jo LLM applications banane mein help karta hai.",
    "RAG ka matlab hai Retrieval Augmented Generation.",
    "Groq ek fast AI inference platform hai."
]

# Embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ChromaDB setup
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("knowledge")

# Documents add karo
embeddings = embedder.encode(documents).tolist()
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(documents))]
)

# Question poocho
question = "RAG kya hai?"
question_embedding = embedder.encode([question]).tolist()

# Relevant document dhundo
results = collection.query(query_embeddings=question_embedding, n_results=1)
context = results['documents'][0][0]

print(f"Context mila: {context}")

# AI ko context ke saath answer do
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": f"Answer based on this context: {context}"},
        {"role": "user", "content": question}
    ]
)

print(f"AI Answer: {response.choices[0].message.content}")