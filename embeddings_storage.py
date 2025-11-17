# embeddings_storage.py - Convert text to vectors and store in ChromaDB

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

def create_embedding_model():
    """
    Load the sentence transformer model for creating embeddings.
    
    Returns:
        SentenceTransformer model
    """
    print("Loading embedding model...")
    
    # This model converts text to 384-dimensional vectors
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("✓ Model loaded successfully!")
    print(f"  Model: all-MiniLM-L6-v2")
    print(f"  Vector dimensions: 384")
    return model

def create_vector_database():
    """
    Initialize ChromaDB for storing vectors.
    
    Returns:
        ChromaDB client
    """
    print("\nInitializing vector database...")
    
    # Create a persistent client (saves to disk)
    client = chromadb.PersistentClient(path="./chroma_db")
    
    print("✓ Database initialized!")
    print(f"  Storage location: ./chroma_db")
    return client

def create_or_get_collection(client, collection_name="documents"):
    """
    Create or retrieve a collection in ChromaDB.
    A collection is like a table that holds related documents.
    
    Args:
        client: ChromaDB client
        collection_name: Name for the collection
    
    Returns:
        Collection object
    """
    print(f"\nSetting up collection: '{collection_name}'")
    
    # Get or create collection
    # This will delete existing collection if it exists (for fresh start)
    try:
        client.delete_collection(name=collection_name)
        print(f"  Deleted existing collection")
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "Document chunks with embeddings"}
    )
    
    print(f"✓ Collection ready!")
    return collection

def embed_and_store_chunks(chunks, model, collection):
    """
    Convert text chunks to vectors and store in database.
    
    Args:
        chunks: List of text chunks
        model: SentenceTransformer model
        collection: ChromaDB collection
    """
    print(f"\nEmbedding {len(chunks)} chunks...")
    
    # Convert all chunks to vectors at once (batch processing)
    embeddings = model.encode(chunks, show_progress_bar=True)
    
    print(f"✓ Created {len(embeddings)} embeddings")
    print(f"  Each embedding: {len(embeddings[0])} dimensions")
    
    # Prepare data for ChromaDB
    # ChromaDB needs: IDs, documents (text), and embeddings (vectors)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    print(f"\nStoring in database...")
    
    # Add to collection
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()  # Convert numpy array to list
    )
    
    print(f"✓ Stored {len(chunks)} chunks in database!")

def test_retrieval(collection, query_text, model, n_results=3):
    """
    Test retrieving similar chunks based on a query.
    
    Args:
        collection: ChromaDB collection
        query_text: Question or search query
        model: SentenceTransformer model
        n_results: Number of results to retrieve
    """
    print(f"\n{'='*60}")
    print("TESTING RETRIEVAL")
    print(f"{'='*60}")
    print(f"\nQuery: '{query_text}'")
    
    # Convert query to vector
    query_embedding = model.encode([query_text])[0]
    
    # Search for similar chunks
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )
    
    print(f"\nFound {len(results['documents'][0])} relevant chunks:")
    print(f"{'-'*60}")
    
    # Display results
    for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
        similarity = 1 - distance  # Convert distance to similarity score
        print(f"\nResult {i+1} (Similarity: {similarity:.3f}):")
        print(f"{doc}")
        print(f"{'-'*60}")

# Main execution
if __name__ == "__main__":
    print("Embeddings & Storage - Testing\n")
    
    # Sample chunks (in real use, these come from document_loader.py)
    sample_chunks = [
        "Artificial Intelligence (AI) is the simulation of human intelligence by machines. AI systems can perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation.",
        
        "Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms that can access data and learn from it.",
        
        "Deep Learning is a subset of machine learning that uses neural networks with multiple layers. These networks can learn complex patterns in large amounts of data. Deep learning has achieved remarkable results in image recognition, natural language processing, and game playing.",
        
        "Neural Networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers. Each connection has a weight that adjusts as learning proceeds.",
        
        "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and generate human language. NLP combines computational linguistics with machine learning and deep learning models."
    ]
    
    # Step 1: Load embedding model
    model = create_embedding_model()
    
    # Step 2: Initialize database
    client = create_vector_database()
    
    # Step 3: Create collection
    collection = create_or_get_collection(client, "test_documents")
    
    # Step 4: Embed and store chunks
    embed_and_store_chunks(sample_chunks, model, collection)
    
    # Step 5: Test retrieval with different queries
    print("\n" + "="*60)
    print("TESTING DIFFERENT QUERIES")
    print("="*60)
    
    # Query 1
    test_retrieval(collection, "What is machine learning?", model, n_results=2)
    
    # Query 2
    test_retrieval(collection, "How do neural networks work?", model, n_results=2)
    
    # Query 3
    test_retrieval(collection, "Tell me about NLP", model, n_results=2)
    
    print("\n✅ Embedding and storage test complete!")
    print(f"\nDatabase location: ./chroma_db")
    print(f"You can delete this folder to reset the database.")