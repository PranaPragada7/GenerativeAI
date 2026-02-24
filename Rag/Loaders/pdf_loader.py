from langchain_community.document_loaders import PyPDFLoader

#Load a PDF file and print the number of documents and the first 50 characters of each document
loader = PyPDFLoader(r"C:\Users\prana\GenAI\Rag\docs\demo_pdf.pdf")
documents = loader.load()

#Checking the number of documents
print("Document Count:", len(documents))

#Print the first 50 characters of each document
for doc in documents:
    print(doc.page_content[:50])
    print("-" * 50)