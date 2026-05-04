from typing import Literal
from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq


class RouterQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    
    datasource: Literal["vectorstore", "websearch"] = Field(
        ..., description="Given a user question choose to route it to web search or a vectorstore."
    )
    
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0).with_structured_output(RouterQuery)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","""You are an expert at routing a user question to a vectorstore or web search.
                     The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
                     Use the vectorstore for questions on these topics. For all else, use web-search."""),
        ("human", "{question}"),
    ]
)

router_chain : RunnableSequence = prompt | llm