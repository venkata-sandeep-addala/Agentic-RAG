from typing import Dict, Any

from graph.state import GraphState
from ingestion import retriever

def retrieve_documents(state: GraphState) -> Dict[str, Any]:
    """ Retrieve relevant documents based on the question in the state. """
    print("---RETRIEVE---")
    retrieved_docs = retriever.invoke(state["question"])
    return {"question": state["question"], "documents": retrieved_docs}