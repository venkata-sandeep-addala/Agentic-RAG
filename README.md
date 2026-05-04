# Agentic-RAG

An implementation of advanced Retrieval-Augmented Generation (RAG) techniques including Corrective RAG (CRAG), Self-RAG, and Adaptive RAG using LangGraph.

## Features

- **Corrective RAG (CRAG)**: Retrieves documents, grades their relevance, generates answers, and corrects hallucinations by re-retrieving or web searching if needed.
- **Self-RAG**: Incorporates self-reflection mechanisms to grade the generated answers for hallucination and relevance to the question.
- **Adaptive RAG**: Routes queries to the most appropriate data source (vectorstore or web search) based on the question content.

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd agentic-rag
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set up environment variables:
   Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=your_endpoint
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_PROJECT="Agentic RAG"
   ```

## Usage

1. Run data ingestion to populate the vectorstore:
   ```bash
   python -m ingestion
   ```

2. Run the main application:
   ```bash
   python -m main
   ```

## Project Structure

- `main.py`: Entry point for running the RAG system.
- `ingestion.py`: Script to load and process documents into the vectorstore.
- `graph/`: Contains the LangGraph implementation.
  - `graph.py`: Defines the graph structure and flow.
  - `state.py`: Defines the state for the graph.
  - `nodes/`: Individual nodes for retrieval, generation, grading, etc.
  - `chains/`: LLM chains for grading, routing, etc.

## Requirements

- Python >= 3.12
- See `pyproject.toml` for full dependencies.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[Add license if applicable]
