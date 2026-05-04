from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field


class HallucinationGrader(BaseModel):
    """Binary score for hallucination check on generated answer."""
    
    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )
    

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0).with_structured_output(HallucinationGrader)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","""You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
     Give a binary score 'yes' or 'no'. 'yes' means that the answer is grounded in / supported by the set of facts. 'no' means that the answer contains hallucinations and is not supported by the set of facts."""),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
    ]
)

hallucination_grader_chain : RunnableSequence = prompt | llm