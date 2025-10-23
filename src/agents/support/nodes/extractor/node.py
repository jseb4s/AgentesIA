from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field 
from agents.support.state import State
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT

class ContactInfo(BaseModel):
    #Esta clase representa la información de contacto de una persona, y el LLM la llenará automáticamente a partir de un texto dado.
    #Sera a su vez la base para el extractor
    """A person's contact information."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")


llm = init_chat_model(model = "gemini-2.5-flash", 
                      model_provider="google_genai",
                      temperature=0
                      )
llm = llm.with_structured_output(ContactInfo)

def extractor(state: State): # Nodo extractor, que extrae información del usuario si no está presente.
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 10:
        schema = llm.invoke([("system", SYSTEM_PROMPT)] + history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state