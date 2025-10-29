from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.conversation.tools import tools
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT
from langchain_core.messages import AIMessage


llm = init_chat_model(model = "gemini-2.5-flash", 
                      model_provider="google_genai",
                      temperature=1
                      )

llm = llm.bind_tools(tools)



def conversation(state: State): # Nodo de conversación, que usa el LLM para responder mensajes del usuario.
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]

    customer_name = state.get("customer_name", "John Doe")
    system_message = f"You are a helpful assistant that can answer questions about the customer {customer_name}."
    ai_message = llm.invoke([("system", SYSTEM_PROMPT), ("user", last_message.text)])
    ai_message = AIMessage(content = ai_message.text) # Sirve para evitar guardar tantos metadatos en el historial
    new_state["messages"] = [ai_message]
    return new_state