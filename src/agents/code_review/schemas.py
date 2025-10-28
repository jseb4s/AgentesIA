from pydantic import BaseModel, Field

class SecurityReview(BaseModel):
    vulnerabilities: list[str] = Field(description="The vulnerabilities in the code", default=None)
    riskLevel: str = Field(description="The risk level of the vulnerabilities", default=None)
    suggestions: list[str] = Field(description="The suggestions for fixing the vulnerabilities", default=None)

class MaintainabilityReview(BaseModel):
    concerns: list[str] = Field(description="The concerns about the code", default=None)
    qualityScore: int = Field(description="The quality score of the code from 1 to 10", default=None, ge=1, le=10)
    recommendations: list[str] = Field(description="The recommendations for improving the code", default=None)