from agents.code_review.state import State
from langchain.chat_models import init_chat_model

llm = init_chat_model(model = "gemini-2.5-flash", 
                      model_provider="google_genai",
                      temperature=0
                      )

def aggregator(state: State):
    security_review = state['security_review']
    maintainability_review = state['maintainability_review']
    messages = [
        ("system", "You are a technical lead summarizing multiple code reviews"),
        ("user", f"Synthesize these code review results into a concise summary with key actions: Security review: {security_review} and Maintainability review: {maintainability_review}")
    ]
    response = llm.invoke(messages)
    return {
        'final_review': response.text
    }