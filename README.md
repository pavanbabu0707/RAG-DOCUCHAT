\# DocuChat - RAG-based Document Q\&A System



A Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions about them using natural language.



\## Features



\- 📄 Document loading and processing (text files, PDFs)

\- ✂️ Intelligent text chunking with overlap

\- 🧠 Vector embeddings using Sentence Transformers

\- 💾 Vector storage with ChromaDB

\- 🔍 Semantic search for relevant context

\- 🤖 Natural language answers using Ollama (Llama 3.2)



\## Technologies Used



\- \*\*Python 3.12\*\*

\- \*\*LangChain\*\* - Framework for LLM applications

\- \*\*ChromaDB\*\* - Vector database for embeddings

\- \*\*Sentence Transformers\*\* - Text embedding models

\- \*\*Ollama\*\* - Local LLM inference

\- \*\*PyPDF\*\* - PDF text extraction



\## Installation



\### Prerequisites



\- Python 3.8+

\- Ollama installed locally



\### Setup



1\. Clone the repository:

```bash

git clone https://github.com/YOUR\_USERNAME/DocuChat-RAG-System.git

cd DocuChat-RAG-System

```



2\. Create virtual environment:

```bash

python -m venv venv

venv\\Scripts\\activate  # Windows

\# source venv/bin/activate  # Mac/Linux

```



3\. Install dependencies:

```bash

pip install langchain langchain-community langchain-text-splitters chromadb pypdf sentence-transformers requests

```



4\. Install Ollama and pull model:

```bash

ollama pull llama3.2

```



\## Usage



\### Test Document Loader

```bash

python document\_loader.py

```



\### Test Embeddings \& Storage

```bash

python embeddings\_storage.py

```



\## Project Structure

```

DocuChat/

├── document\_loader.py      # Document loading and chunking

├── embeddings\_storage.py   # Vector embeddings and ChromaDB storage

├── test\_setup.py          # Installation verification

├── sample\_doc.txt         # Sample document for testing

└── README.md             # This file

```



\## How It Works



1\. \*\*Document Loading\*\*: Text is extracted from documents

2\. \*\*Chunking\*\*: Documents are split into manageable chunks with overlap

3\. \*\*Embedding\*\*: Each chunk is converted to a 384-dimensional vector

4\. \*\*Storage\*\*: Vectors are stored in ChromaDB for fast retrieval

5\. \*\*Query\*\*: User questions are converted to vectors and matched with similar chunks

6\. \*\*Generation\*\*: Relevant chunks are sent to Ollama to generate answers



\## Roadmap



\- \[ ] PDF support

\- \[ ] Web interface (Streamlit/Gradio)

\- \[ ] Conversation history

\- \[ ] Multiple document support

\- \[ ] Source citation in answers

\- \[ ] Deployment



\## Contributing



Contributions are welcome! Feel free to open issues or submit pull requests.



\## License



MIT License



\## Author



Built as a learning project for AI engineering portfolio.



\## Acknowledgments



\- Anthropic's Claude for development assistance

\- LangChain community

\- Sentence Transformers team

