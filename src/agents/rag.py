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
    phone: str
    my_age: str


# RAG con Chaining de nodos, es decir, pasos secuenciales. Cada paso usualmente usa un LLM.
# Este caso se usa mucho en RRSS para generar tweets e imagenes a partir de tweets.

from pydantic import BaseModel, Field
class ContactInfo(BaseModel):
    #Esta clase representa la información de contacto de una persona, y el LLM la llenará automáticamente a partir de un texto dado.
    #Sera a su vez la base para el extractor
    """A person's contact information."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")


llm_with_structured_output = init_chat_model(model = "gemini-2.5-flash", 
                      model_provider="google_genai",
                      temperature=0
                      )
llm_with_structured_output = llm_with_structured_output.with_structured_output(ContactInfo)


# El nodo extractor no es conversacional, sino que extrae información del usuario a partir de su mensaje.
# Evalua la información que hay en el historial de la conversación y extrae la información que falta.
def extractor(state: State): # Nodo extractor, que extrae información del usuario si no está presente.
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 10:
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state

def conversation(state: State): # Nodo de conversación, que usa el LLM para responder mensajes del usuario.
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]

    customer_name = state.get("customer_name", "John Doe")
    system_message = f"You are a helpful assistant that can answer questions about the customer {customer_name}."
    ai_message = llm.invoke([("system", system_message), ("user", last_message.text)])
    new_state["messages"] = [ai_message]
    return new_state

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)
builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()