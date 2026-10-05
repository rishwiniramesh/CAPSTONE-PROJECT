from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all readable text from a PDF uploaded through Streamlit.
    """

    reader = PdfReader(uploaded_file)

    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text.strip())

    return "\n\n".join(pages)