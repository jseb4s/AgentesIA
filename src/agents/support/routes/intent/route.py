from pydantic import BaseModel, Field
from typing import Literal
from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.routes.intent.prompt import SYSTEM_PROMPT

class RouteIntent(BaseModel):
    """contact information for a person"""
    step: Literal["conversation", "booking"] = Field(
        None, description="The next step in the routing process" 
# None aqui es como el valor por defecto. Se podria reemplazar por "conversation" o "booking", por ejemplo.
    )

"""
RouteIntent: Es un modelo que representa la intención de enrutamiento
step: Un campo que solo puede tener dos valores: "conversation" o "booking"
Literal: Restringe los valores posibles (solo esas dos cadenas)
Field(..., description=...): Añade metadata que ayuda a un LLM a entender cuándo usar cada opción
"""


llm = init_chat_model("google_genai:gemini-2.5-flash", temperature=0)
llm = llm.with_structured_output(schema=RouteIntent)

def intent_route(state: State) -> Literal["conversation", "booking"]:
    history = state["messages"]
    schema = llm.invoke([("system", SYSTEM_PROMPT)] + history)
    if schema.step is not None:
        return schema.step
    return "conversation"  # Default route if none is determined