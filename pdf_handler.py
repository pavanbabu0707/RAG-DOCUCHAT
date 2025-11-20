# pdf_handler.py - Handle PDF document processing

import pypdf
import os

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        Extracted text as a string, or None if failed
    """
    print(f"Loading PDF: {pdf_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"✗ Error: File not found at {pdf_path}")
            return None
        
        # Open the PDF
        with open(pdf_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = pypdf.PdfReader(file)
            
            # Get number of pages
            num_pages = len(pdf_reader.pages)
            print(f"  Found {num_pages} pages")
            
            # Extract text from all pages
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                text += page_text + "\n\n"
                
                # Show progress for large PDFs
                if (page_num + 1) % 10 == 0:
                    print(f"  Processed {page_num + 1}/{num_pages} pages...")
            
            print(f"✓ PDF loaded successfully!")
            print(f"  Total pages: {num_pages}")
            print(f"  Total characters: {len(text)}")
            
            return text
    
    except pypdf.errors.PdfReadError as e:
        print(f"✗ Error reading PDF: {e}")
        print("  The file might be corrupted or password-protected")
        return None
    
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None

def load_document(file_path):
    """
    Load a document (supports both .txt and .pdf files).
    Automatically detects file type based on extension.
    
    Args:
        file_path: Path to the document
    
    Returns:
        Extracted text as string, or None if failed
    """
    # Get file extension
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    
    print(f"\n{'='*60}")
    print("DOCUMENT LOADING")
    print(f"{'='*60}")
    print(f"File: {file_path}")
    print(f"Type: {extension}")
    
    # Route to appropriate handler
    if extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif extension == '.txt':
        # Use our existing text file loader
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            print(f"✓ Text file loaded successfully!")
            print(f"  Total characters: {len(text)}")
            return text
        except Exception as e:
            print(f"✗ Error loading text file: {e}")
            return None
    else:
        print(f"✗ Unsupported file type: {extension}")
        print(f"  Supported types: .pdf, .txt")
        return None

# Test the PDF handler
if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("PDF HANDLER - TESTING")
    print("="*60)
    
    # Test with a sample PDF (you'll need to provide one)
    if len(sys.argv) > 1:
        # If user provides file path as command line argument
        file_path = sys.argv[1]
    else:
        # Default test file
        file_path = input("\nEnter path to PDF or TXT file to test: ").strip()
    
    if file_path:
        text = load_document(file_path)
        
        if text:
            print(f"\n{'='*60}")
            print("EXTRACTED TEXT PREVIEW (first 500 characters)")
            print(f"{'='*60}")
            print(text[:500])
            print("\n[...]")
            
            print(f"\n✅ Success! Extracted {len(text)} characters from document.")
        else:
            print("\n✗ Failed to extract text from document.")
    else:
        print("\n✗ No file path provided.")