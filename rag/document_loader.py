import os
import chromadb
import pypdf

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Chunks text into smaller chunks of a specified size with an overlap."""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

def load_pdf(documents: list[str], chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """Loads pdf into a list of dictionaries """
    listOfDocs = []
    for document in documents:
        reader = pypdf.PdfReader(document)
        docDict = {}
        docDict["text"] = []
        docDict["name"] = os.path.basename(document)
        for page in reader.pages:
            docDict["text"]+=chunk_text(page.extract_text(), chunk_size, overlap)
        listOfDocs.append(docDict)
    return listOfDocs

if __name__ == "__main__":
    docs = load_pdf(["pdfs/rubiks_cube.pdf"])
    print(f"Document: {docs[0]['name']}")
    print(f"Nombre de chunks: {len(docs[0]['text'])}")
    print(f"Premier chunk:\n{docs[0]['text'][0][:200]}...")