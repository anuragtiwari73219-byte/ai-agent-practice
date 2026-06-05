from groq import Groq
import chromadb
from dotenv import load_dotenv
import os 
load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
# chroma_client=chromadb.Client()
chroma_client = chromadb.PersistentClient(path="./memory_db")
collection=chroma_client.get_or_create_collection("chat_memory")
def save_memory(user_msg,assistant_msg):
    collection.add(
        documents=[f"User:{user_msg} Assistent: {assistant_msg}"],
        ids=[str(collection.count())]
        )
def get_memory(query):
    results=collection.query(
        query_texts=[query],
        n_results=2
    )
    return results['documents'][0] if results['documents'] else[]
def chat (user_message):
    memories=get_memory(user_message)
    memory_context="\n".join(memories) if memories else "No previous memory"

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":f"previous converstions:\n{memory_context}"},
            {"role":"user","content": user_message}
        ]
    )
    assistant_message=response.choices[0].message.content
    save_memory(user_message,assistant_message)
    return assistant_message
while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    response = chat(user_input)
    print(f"AI: {response}")


            