from typing import TypedDict, List

class GraphState(TypedDict):
    """State of the graph."""
    question: str
    generation: str
    web_search: bool
    documents: List[str]
    
    