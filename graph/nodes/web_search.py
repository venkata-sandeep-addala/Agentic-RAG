from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

from graph.state import GraphState
from langchain_tavily import TavilySearch
from langchain_classic.schema import Document


tavily_web_search = TavilySearch(max_results=1)



def web_search(state: GraphState) -> Dict[str, Any]:
    """Perform a web search based on the question."""
    print("---WEB SEARCH---")
    question = state["question"]
    
    if "documents" in state: # if the route to web search in first time then give error
        documents = state["documents"]
    else:
        documents = None
    
    tavily_search_results = tavily_web_search.invoke(question)
    joined_tavily_results = "\n".join([result['results'][-1]['content'] for result in tavily_search_results])
    
    doc = Document(page_content=joined_tavily_results)
    
    if documents:
        documents.append(doc)
    else:
        documents = [doc]
        
    return {"question": question, "documents": documents}


if __name__ == "__main__":
    # Example usage
    result = tavily_web_search.invoke("What is the capital of France?")
    print(result)