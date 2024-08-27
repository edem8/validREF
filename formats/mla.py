import re
from pdfminer.high_level import extract_text


def extract_mla_citations(pdf_path):
    # Extract text from the provided PDF
    content = extract_text(pdf_path)

    # Regular expression to match MLA citations
    mla_pattern = r'\((?:[A-Za-z\s&.,]+(?: \d{1,4})?(?:; [A-Za-z\s&.,]+(?: \d{1,4})?)*)\)|(?:\["?[A-Za-z\s&.,]+"?, \d{1,4}\])'

    # Find all matches
    citations = re.findall(mla_pattern, content)

    return citations
