# document_loader.py - Load and split documents into chunks

from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_text_file(file_path):
    """
    Load a text file and return its contents.
    
    Args:
        file_path: Path to the text file
    
    Returns:
        String containing the file contents
    """
    print(f"Loading file: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        print(f"✓ File loaded successfully! Length: {len(text)} characters")
        return text
    except FileNotFoundError:
        print(f"✗ Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return None

def split_into_chunks(text, chunk_size=500, chunk_overlap=50):
    """
    Split text into smaller chunks for processing.
    
    Args:
        text: The text to split
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    print(f"\nSplitting text into chunks...")
    print(f"Chunk size: {chunk_size} characters")
    print(f"Chunk overlap: {chunk_overlap} characters")
    
    # Create the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    
    # Split the text
    chunks = text_splitter.split_text(text)
    
    print(f"✓ Created {len(chunks)} chunks")
    return chunks

def display_chunks(chunks):
    """
    Display all chunks with their index and length.
    
    Args:
        chunks: List of text chunks
    """
    print("\n" + "="*60)
    print("DOCUMENT CHUNKS")
    print("="*60)
    
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ({len(chunk)} characters) ---")
        print(chunk)
        print("-" * 60)

# Main execution
if __name__ == "__main__":
    print("Document Loader - Testing\n")
    
    # Step 1: Load the document
    text = load_text_file("sample_doc.txt")
    
    if text:
        # Step 2: Split into chunks
        chunks = split_into_chunks(text, chunk_size=300, chunk_overlap=50)
        
        # Step 3: Display the chunks
        display_chunks(chunks)
        
        print(f"\n✅ Success! Created {len(chunks)} chunks from the document.")