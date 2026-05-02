
from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.nodes.web_search import web_search
from graph.nodes.grade_documents import grade_documents
from graph.nodes.generate import generate
from graph.nodes.retrieve import retrieve_documents
from graph.consts import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEB_SEARCH


def decide_to_generate(state: GraphState):
    """ Decide whether to call the Generate Node or Web Search node based on the web_search field."""
    
    if state['web_search']:
        return WEB_SEARCH
    else:
        return GENERATE
    
builder = StateGraph(GraphState)
builder.add_node(RETRIEVE, retrieve_documents)
builder.add_node(GRADE_DOCUMENTS, grade_documents)
builder.add_node(GENERATE, generate)
builder.add_node(WEB_SEARCH, web_search)
builder.set_entry_point(RETRIEVE)
builder.add_edge(RETRIEVE, GRADE_DOCUMENTS)
builder.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate, {WEB_SEARCH: WEB_SEARCH, GENERATE: GENERATE})
builder.add_edge(WEB_SEARCH, GENERATE)
builder.add_edge(GENERATE, END)

graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


# response = graph.invoke({"question": "what is agent memory?"})