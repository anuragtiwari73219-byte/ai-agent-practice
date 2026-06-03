from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    message: str
    response: str

def decide(state: AgentState):
    print(f"Deciding for: {state['message']}")
    return {"response": "deciding"}

def route(state: AgentState):
    if "weather" in state["message"]:
        return "use_tool"
    else:
        return "direct_answer"

def use_tool(state: AgentState):
    print(f"Tool use kar raha hoon: {state['message']}")
    return {"response": "Weather in Kanpur: sunny 30C"}

def direct_answer(state: AgentState):
    print(f"Direct answer: {state['message']}")
    return {"response": "Direct answer diya"}

graph = StateGraph(AgentState)

graph.add_node("decide", decide)
graph.add_node("use_tool", use_tool)
graph.add_node("direct_answer", direct_answer)

graph.add_conditional_edges("decide", route, {
    "use_tool": "use_tool",
    "direct_answer": "direct_answer"
})
graph.add_edge("use_tool", END)
graph.add_edge("direct_answer", END)

graph.set_entry_point("decide")
app = graph.compile()

# result = app.invoke({"message": "weather in Kanpur", "response": ""})
result = app.invoke({"message": "What is Python?", "response": ""})
print(result)