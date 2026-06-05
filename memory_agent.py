from groq import Groq 
from dotenv import load_dotenv
import os 

load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
conversation_history=[]
def chat(user_message):
    conversation_history.append({"role":"user","content":user_message})
    responce=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history
    )
    assistant_message=responce.choices[0].message.content
    conversation_history.append({"role":"assistant","content":assistant_message})
    return assistant_message
while True:
    user_input=input("you:")
    if user_input=="quit":
        break
    response=chat(user_input)
    print(f"AI:{response}")