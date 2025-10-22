from langgraph.graph import MessagesState # Messages State permiten manejar historiales de mensajes de forma sencilla
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import random

llm = init_chat_model(model = "gemini-2.5-flash", 
                      model_provider="google_genai",
                      temperature=1
                      )

file_search_tool = {
    "type": "file_search",
    "vector_store_ids": ["vs_376gdhd772129hhh92"] # Este id se obtiene al crear el vector store en la web deOpenAi
}

llm = llm.bind_tools([file_search_tool])

class State(MessagesState):
    customer_name: str
    my_age: int

def node_1(state: State):
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "John Doe"
    else:
        new_state["my_age"] = random.randint(18, 99)

    history = state["messages"]
    last_message = history[-1]
    ai_message = llm.invoke(last_message.text)
    new_state["messages"] = [ai_message]
    return new_state

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()