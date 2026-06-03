from langgraph.graph import StateGraph,END
from typing import TypedDict
class AgentState(TypedDict):
    message:str
    response:str
def validate(state: AgentState):
    print(f"validating message:{state['message']}")
    return {"response":"validation done "}
def process(state: AgentState):
    print(f" message mila :{state['message']}")
    return {"response":"proceesing done"}
def respond(state: AgentState):
    print(f" response:{state['response']}")
    return{}
graph=StateGraph(AgentState)

graph.add_node("validate",validate)
graph.add_node("process",process)
graph.add_node("respond",respond)

graph.add_edge("validate","process")
graph.add_edge("process","respond")
graph.add_edge("respond",END)

graph.set_entry_point("validate")
app=graph.compile()
result=app.invoke({"message":"hello","response":""})


