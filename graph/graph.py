
from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.nodes.web_search import web_search
from graph.nodes.grade_documents import grade_documents
from graph.nodes.generate import generate
from graph.nodes.retrieve import retrieve_documents
from graph.chains.hallucination_grader import hallucination_grader_chain
from graph.chains.answer_grader import answer_grader_chain
from graph.chains.router import router_chain
from graph.consts import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEB_SEARCH


def decide_to_generate(state: GraphState):
    """ Decide whether to call the Generate Node or Web Search node based on the web_search field."""
    
    if state['web_search']:
        return WEB_SEARCH
    else:
        return GENERATE
    
def grade_generation_grounded_in_documents_and_question(state: GraphState):
    """ Grade whether the generation is grounded in the retrieved documents and the generation answer's the question."""
    print("---CHECK HALLUCINATIONS---")
    question = state['question']
    generation = state['generation']
    documents = state['documents']
    
    hallucination_grade = hallucination_grader_chain.invoke({
        "generation": generation, "documents": documents
    })
    
    
    if hallucination_grade.binary_score == 'yes':
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        answer_grade = answer_grader_chain.invoke({
            "question": question, "generation": generation
        })
        if answer_grade.binary_score == 'yes':
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"
    

def decide_route_based_on_question(state: GraphState):
    """ Decide whether to route to web search or vectorstore based on the question."""
    print("---ROUTE QUESTION---")
    question = state['question']
    router_decision = router_chain.invoke({"question": question})
    if router_decision.datasource == "websearch":
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return WEB_SEARCH
    elif router_decision.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE
    
    
    
    
builder = StateGraph(GraphState)
builder.add_node(RETRIEVE, retrieve_documents)
builder.add_node(GRADE_DOCUMENTS, grade_documents)
builder.add_node(GENERATE, generate)
builder.add_node(WEB_SEARCH, web_search)
builder.add_edge(RETRIEVE, GRADE_DOCUMENTS)
builder.set_conditional_entry_point(decide_route_based_on_question, {WEB_SEARCH: WEB_SEARCH, RETRIEVE: RETRIEVE})
builder.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate, {WEB_SEARCH: WEB_SEARCH, GENERATE: GENERATE})
builder.add_conditional_edges(GENERATE, grade_generation_grounded_in_documents_and_question, {"useful": END, "not useful": WEB_SEARCH, "not supported": GENERATE})
builder.add_edge(WEB_SEARCH, GENERATE)
builder.add_edge(GENERATE, END)

graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


# response = graph.invoke({"question": "what is agent memory?"})