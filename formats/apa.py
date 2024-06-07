import re
from pdfminer.high_level import extract_text


def extract_apa_citations(pdf_path):

    # Extract text from provided pdf
    content = extract_text(pdf_path)
    
    # Regular expression to match APA citations
    apa_pattern = (
        r"\([A-Za-z &.,]+(?: et al\.)?, \d{4}(?:; [A-Za-z &.,]+(?: et al\.)?, \d{4})*\)"
    )

    # Find all matches
    citations = re.findall(apa_pattern, content)

    return citations


