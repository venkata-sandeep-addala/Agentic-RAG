from dotenv import load_dotenv

load_dotenv()

from graph.graph import graph

if __name__ == "__main__":
    print("Hello Advanced RAG")
    print(graph.invoke(input={"question": "IPL 2026?"})['generation'])