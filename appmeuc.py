from PIL import Image
import pytesseract
import pdf2image

# Convert PDF to images
pages = pdf2image.convert_from_path(pdf_path)

# Extract text from each page
extracted_text = ""
for page in pages:
    text = pytesseract.image_to_string(page, lang='por')
    extracted_text += text + "\n"

extracted_text
