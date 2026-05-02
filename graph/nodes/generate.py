from graph.state import GraphState
from graph.chains.generation import generation_chain

def generate(state: GraphState):
    """Generate an answer to the question using the generation chain."""
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    
    generation = generation_chain.invoke({"question": question, "context": documents})
    
    return {"generation": generation, "question": question, "documents": documents}