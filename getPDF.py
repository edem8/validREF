from langchain_community.document_loaders import PyPDFLoader

def get_pdf(pdf_doc):

    pdf_loader = PyPDFLoader(pdf_doc)
    pages = pdf_loader.load_and_split()

    return pages
    