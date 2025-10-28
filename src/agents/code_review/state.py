from typing import TypedDict
from agents.code_review.schemas import SecurityReview, MaintainabilityReview

class State(TypedDict):
    code: str
    security_review: SecurityReview
    maintainability_review: MaintainabilityReview
    final_review: str