from langgraph.graph import StateGraph, START, END
from agents.code_review.state import State
from agents.code_review.nodes.security_review.node import security_review
from agents.code_review.nodes.maintainability_review.node import maintainability_review
from agents.code_review.nodes.aggregator.node import aggregator

builder = StateGraph(State)

builder.add_node('security_review', security_review)
builder.add_node('maintainability_review', maintainability_review)
builder.add_node('aggregator', aggregator)

builder.add_edge(START, 'security_review')
builder.add_edge(START, 'maintainability_review')
builder.add_edge("security_review", "aggregator")
builder.add_edge("maintainability_review", "aggregator")
builder.add_edge('aggregator', END)
agent = builder.compile()