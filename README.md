&nbsp;DocuChat   RAG based Document Q\&A System



A Retrieval Augmented Generation (RAG) system that allows users to upload documents and ask questions about them using natural language.



&nbsp;  Features



&nbsp; 📄 Document loading and processing (text files, PDFs)

&nbsp; ✂️ Intelligent text chunking with overlap

&nbsp; 🧠 Vector embeddings using Sentence Transformers

&nbsp; 💾 Vector storage with ChromaDB

&nbsp; 🔍 Semantic search for relevant context

&nbsp; 🤖 Natural language answers using Ollama (Llama 3.2)



&nbsp;  Technologies Used



&nbsp;   Python 3.12  

&nbsp;   LangChain     Framework for LLM applications

&nbsp;   ChromaDB     Vector database for embeddings

&nbsp;   Sentence Transformers     Text embedding models

&nbsp;   Ollama     Local LLM inference

&nbsp;   PyPDF     PDF text extraction



&nbsp;  Installation



&nbsp;   Prerequisites



&nbsp; Python 3.8+

&nbsp; Ollama installed locally



&nbsp;   Setup



1\. Clone the repository:

```bash

git clone https://github.com/YOUR\_USERNAME/DocuChat RAG System.git

cd DocuChat RAG System

```



2\. Create virtual environment:

```bash

python  m venv venv

venv\\Scripts\\activate    Windows

&nbsp; source venv/bin/activate    Mac/Linux

```



3\. Install dependencies:

```bash

pip install langchain langchain community langchain text splitters chromadb pypdf sentence transformers requests

```



4\. Install Ollama and pull model:

```bash

ollama pull llama3.2

```



&nbsp;  Usage



&nbsp;   Test Document Loader

```bash

python document\_loader.py

```



&nbsp;   Test Embeddings \& Storage

```bash

python embeddings\_storage.py

```



&nbsp;  Project Structure

```

DocuChat/

├── document\_loader.py        Document loading and chunking

├── embeddings\_storage.py     Vector embeddings and ChromaDB storage

├── test\_setup.py            Installation verification

├── sample\_doc.txt           Sample document for testing

└── README.md               This file

```



&nbsp;  How It Works



1\.   Document Loading  : Text is extracted from documents

2\.   Chunking  : Documents are split into manageable chunks with overlap

3\.   Embedding  : Each chunk is converted to a 384 dimensional vector

4\.   Storage  : Vectors are stored in ChromaDB for fast retrieval

5\.   Query  : User questions are converted to vectors and matched with similar chunks

6\.   Generation  : Relevant chunks are sent to Ollama to generate answers



&nbsp;  Roadmap



&nbsp;   PDF support

&nbsp;   Web interface (Streamlit/Gradio)

&nbsp;   Conversation history

&nbsp;   Multiple document support

&nbsp;   Source citation in answers

&nbsp;   Deployment



&nbsp;  Contributing



Contributions are welcome! Feel free to open issues or submit pull requests.



&nbsp;  License



MIT License



&nbsp;  Author



Built as a learning project for AI engineering portfolio.



&nbsp;  Acknowledgments



&nbsp; Anthropic's Claude for development assistance

&nbsp; LangChain community

&nbsp; Sentence Transformers team

