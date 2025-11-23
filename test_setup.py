# test_setup.py - Testing our installations

print("Testing imports...")

# Test 1: LangChain
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✓ LangChain works!")
except ImportError as e:
    print(f"✗ LangChain error: {e}")

# Test 2: ChromaDB
try:
    import chromadb
    print("✓ ChromaDB works!")
except ImportError as e:
    print(f"✗ ChromaDB error: {e}")

# Test 3: Sentence Transformers
try:
    from sentence_transformers import SentenceTransformer
    print("✓ Sentence Transformers works!")
except ImportError as e:
    print(f"✗ Sentence Transformers error is wrong: {e}")

# Test 4: PyPDF
try:
    import pypdf
    print("✓ PyPDF works!")
except ImportError as e:
    print(f"✗ PyPDF error: {e}")

# Test 5: Requests
try:
    import requests
    print("✓ Requests works!")
except ImportError as e:
    print(f"✗ Requests error: {e}")

# Test 6: Ollama (checking if it's running)
try:
    import requests
    response = requests.get("http://localhost:11434")
    if response.status_code == 200:
        print("✓ Ollama is running!")
    else:
        print("✗ Ollama is not responding properly")
except Exception as e:
    print(f"✗ Ollama error: {e}")
    print("  Tip: Make sure Ollama app is running in the background")

print("\n✅ Setup test complete!")