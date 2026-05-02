from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


llm = ChatGroq(model="llama-3.3-70b-versatile")

# RAG prompt template
template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Keep your answer concise.

Context: {context}

Question: {question}

Answer: """

prompt = ChatPromptTemplate.from_template(template)

generation_chain : RunnableSequence = prompt | llm | StrOutputParser()