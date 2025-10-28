from langchain.chat_models import init_chat_model
from agents.code_review.state import State
from agents.code_review.schemas import SecurityReview



llm = init_chat_model(model = "gemini-2.5-flash", 
                      model_provider="google_genai",
                      temperature=0
                      )

def security_review(state: State):
    code = state['code']
    messages = [
        ("system", "You are an expert in code security. Focus on identifying security vulnerabilities, injection risks, and authentication issues."),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(SecurityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'security_review': schema
    }