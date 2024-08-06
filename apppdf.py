import PyPDF2

# Path to the PDF file
pdf_path = "meupdf.pdf"

# Read the PDF file
with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    text = ""
    for page in range(num_pages):
        text += reader.pages[page].extract_text()

text
print(text)