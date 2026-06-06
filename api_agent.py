from fastapi import FastAPI
from groq import Groq 
from dotenv import load_dotenv
import os 
load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
app=FastAPI()

@app.get("/")
def home ():
    return {"message": "Agent API is running"} 
@app.get("/ask")
def ask (question:str):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":question}]
    )
    answer=response.choices[0].message.content
    return{"question": question,"answer": answer}

