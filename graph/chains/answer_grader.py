from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence


class AnswerGrader(BaseModel):
    """Binary score for relevance check on generated answer."""
    
    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )
    

llm = ChatGroq(model="llama-3.3-70b-versatile").with_structured_output(AnswerGrader)



prompt = ChatPromptTemplate.from_messages(
    [
        ("system","""You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question.""")
        ("user", """User question: \n\n {question} \n\n LLM Generation: \n\n {generation}""")
    ]
)


answer_grader_chain : RunnableSequence = prompt | llm