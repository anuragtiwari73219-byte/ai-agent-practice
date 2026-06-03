from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calculate(expression):
    return str(eval(expression))

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a math expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression like 2+2"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

messages = [{"role": "user", "content": "What is 1234 * 5678?"}]

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools
)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
result = calculate(args["expression"])

print(f"Expression: {args['expression']}")
print(f"Answer: {result}")