from graph.state import GraphState
from graph.chains.retriever_grader import retriever_grader_chain


def grade_documents(state: GraphState):
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """
    question = state["question"]
    documents = state["documents"]
    
    web_search = False
    filtered_documents = []
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    
    for doc in documents:
        grade = retriever_grader_chain.invoke({"question": question, "documents": doc.page_content})
        if grade.binary_score.lower() == "no":
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            web_search = True
            continue
        else:
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_documents.append(doc)
            
    return {"documents": filtered_documents, "web_search": web_search, "question": question}