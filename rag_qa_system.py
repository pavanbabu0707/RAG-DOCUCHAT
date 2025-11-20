# rag_qa_system.py - Complete RAG Q&A System

from document_loader import split_into_chunks
from pdf_handler import load_document
from embeddings_storage import create_embedding_model, create_vector_database, create_or_get_collection
from sentence_transformers import SentenceTransformer
import requests
import json

def embed_document(file_path, model, collection, chunk_size=500, chunk_overlap=50):
    """
    Load a document, chunk it, embed it, and store in database.
    
    Args:
        file_path: Path to document
        model: Sentence transformer model
        collection: ChromaDB collection
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
    
    Returns:
        Number of chunks created
    """
    print(f"\n{'='*60}")
    print("DOCUMENT PROCESSING")
    print(f"{'='*60}")
    
    # Step 1: Load document (supports PDF and TXT)
    text = load_document(file_path)
    if not text:
        return 0
    
    # Step 2: Split into chunks
    chunks = split_into_chunks(text, chunk_size, chunk_overlap)
    
    # Step 3: Create embeddings
    print(f"\nCreating embeddings for {len(chunks)} chunks...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    
    # Step 4: Store in database
    print(f"\nStoring in vector database...")
    ids = [f"doc_chunk_{i}" for i in range(len(chunks))]
    
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )
    
    print(f"✓ Successfully processed document!")
    print(f"  Total chunks: {len(chunks)}")
    print(f"  Chunk size: {chunk_size} characters")
    print(f"  Overlap: {chunk_overlap} characters")
    
    return len(chunks)

def retrieve_relevant_chunks(query, model, collection, n_results=3):
    """
    Find the most relevant chunks for a query.
    
    Args:
        query: User's question
        model: Sentence transformer model
        collection: ChromaDB collection
        n_results: Number of chunks to retrieve
    
    Returns:
        List of relevant chunk texts and their similarity scores
    """
    # Convert query to embedding
    query_embedding = model.encode([query])[0]
    
    # Search database
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )
    
    # Extract chunks and calculate similarity scores
    chunks = results['documents'][0]
    distances = results['distances'][0]
    similarities = [1 - d for d in distances]  # Convert distance to similarity
    
    return chunks, similarities

def generate_answer_with_ollama(query, context_chunks, model_name="llama3.2"):
    """
    Generate an answer using Ollama with retrieved context.
    
    Args:
        query: User's question
        context_chunks: List of relevant text chunks
        model_name: Ollama model to use
    
    Returns:
        Generated answer
    """
    # Combine context chunks into one text
    context = "\n\n".join([f"Context {i+1}:\n{chunk}" for i, chunk in enumerate(context_chunks)])
    
    # Create the prompt
    prompt = f"""You are a helpful assistant answering questions based on the provided context. 
Use ONLY the information from the context below to answer the question. 
If the answer cannot be found in the context, say "I cannot find this information in the provided document."

Context:
{context}

Question: {query}

Answer:"""
    
    # Call Ollama API
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False  # Get complete response at once
    }
    
    try:
        print("\nGenerating answer with Ollama...")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        answer = result['response']
        
        return answer
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}\nMake sure Ollama is running."

def display_answer_with_sources(query, answer, chunks, similarities):
    """
    Display the answer and source chunks nicely formatted.
    
    Args:
        query: User's question
        answer: Generated answer
        chunks: Source chunks used
        similarities: Similarity scores for each chunk
    """
    print(f"\n{'='*60}")
    print("ANSWER")
    print(f"{'='*60}")
    print(f"\nQuestion: {query}")
    print(f"\nAnswer:\n{answer}")
    
    print(f"\n{'='*60}")
    print("SOURCE CHUNKS (Retrieved Context)")
    print(f"{'='*60}")
    
    for i, (chunk, similarity) in enumerate(zip(chunks, similarities)):
        print(f"\nSource {i+1} (Relevance: {similarity:.2%}):")
        print(f"{chunk}")
        print(f"{'-'*60}")

def interactive_qa_session(model, collection):
    """
    Run an interactive Q&A session where users can ask multiple questions.
    
    Args:
        model: Sentence transformer model
        collection: ChromaDB collection
    """
    print(f"\n{'='*60}")
    print("INTERACTIVE Q&A SESSION")
    print(f"{'='*60}")
    print("\nYou can now ask questions about your document!")
    print("Type 'quit' or 'exit' to end the session.\n")
    
    while True:
        # Get user question
        query = input("Your question: ").strip()
        
        # Check for exit
        if query.lower() in ['quit', 'exit', 'q']:
            print("\nEnding Q&A session. Goodbye!")
            break
        
        # Skip empty queries
        if not query:
            continue
        
        print(f"\n{'~'*60}")
        
        # Step 1: Retrieve relevant chunks
        print("Searching document for relevant information...")
        chunks, similarities = retrieve_relevant_chunks(query, model, collection, n_results=3)
        
        print(f"✓ Found {len(chunks)} relevant chunks")
        
        # Step 2: Generate answer
        answer = generate_answer_with_ollama(query, chunks)
        
        # Step 3: Display results
        display_answer_with_sources(query, answer, chunks, similarities)
        
        print(f"\n{'~'*60}\n")

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("RAG Q&A SYSTEM")
    print("="*60)
    
    # Configuration
    DOCUMENT_PATH = "sample_doc.txt"  # or "your_document.pdf"
    COLLECTION_NAME = "qa_documents"
    CHUNK_SIZE = 400
    CHUNK_OVERLAP = 50
    
    # You can also ask user for file path
    print("\nDefault document:", DOCUMENT_PATH)
    user_file = input("Enter different file path (or press Enter to use default): ").strip()
    if user_file:
        DOCUMENT_PATH = user_file
    
    # Step 1: Initialize components
    print("\nInitializing system...")
    model = create_embedding_model()
    client = create_vector_database()
    collection = create_or_get_collection(client, COLLECTION_NAME)
    
    # Step 2: Process document
    num_chunks = embed_document(
        DOCUMENT_PATH, 
        model, 
        collection,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    if num_chunks == 0:
        print("\n✗ Failed to process document. Exiting.")
        exit(1)
    
    # Step 3: Run some test queries first
    print(f"\n{'='*60}")
    print("RUNNING TEST QUERIES")
    print(f"{'='*60}")
    
    test_queries = [
        "What is artificial intelligence?",
        "Explain machine learning",
        "How do neural networks work?"
    ]
    
    for query in test_queries:
        print(f"\n{'~'*60}")
        print(f"Test Query: {query}")
        print(f"{'~'*60}")
        
        # Retrieve chunks
        chunks, similarities = retrieve_relevant_chunks(query, model, collection, n_results=2)
        
        # Generate answer
        answer = generate_answer_with_ollama(query, chunks)
        
        # Display
        display_answer_with_sources(query, answer, chunks, similarities)
    
    # Step 4: Interactive session
    print(f"\n{'='*60}")
    print("Test queries complete!")
    print(f"{'='*60}")
    
    user_input = input("\nWould you like to start an interactive Q&A session? (yes/no): ").strip().lower()
    
    if user_input in ['yes', 'y']:
        interactive_qa_session(model, collection)
    else:
        print("\nExiting. Thank you!")