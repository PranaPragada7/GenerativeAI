from langchain_community.document_loaders import TextLoader

#Load a text file and print the number of documents and the first 50 characters of each document
loader = TextLoader(r"C:\Users\prana\GenAI\Rag\docs\mlk.txt", encoding="utf-8")
documents = loader.load()

print("Document Count:", len(documents))
for doc in documents:
    print(doc.page_content[:50])
    print("-" * 50)