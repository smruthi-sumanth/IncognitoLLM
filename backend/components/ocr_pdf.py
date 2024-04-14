import tempfile
from ocrmypdf import ocr
from PIL import Image
from anonymize import analyze_text
from pathlib import Path
from pypdf import PdfReader
def pdf_to_text(pdf_file):
    """
    Convert a PDF file to text using OCR.

    Args:
        pdf_file (bytes): The uploaded PDF file.

    Returns:
        PdfReader: The extracted text from the PDF file.
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        tmp_pdf.write(pdf_file)
        tmp_pdf.flush()
        out_text = ""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_output:
            ocr(tmp_pdf.name, tmp_output.name, skip_text=True, use_threads=True, language="eng+kan")
            test = open("test.pdf", "wb")
            with open(tmp_output.name, "rb") as file:
                reader = PdfReader(file)
                analyze_text(file.read())
                for page in reader.pages:
                    out_text = '\n\n'.join([out_text, page.extract_text()])

        return out_text

def png_to_pdf(png_file):
    """
    Convert a PNG file to PDF.

    Args:
        png_file (bytes): The uploaded PNG file.

    Returns:
        str: The path to the converted PDF file.
    """
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_png:
        tmp_png.write(png_file)
        tmp_png.flush()

        pdf_path = tmp_png.name.replace(".png", ".pdf")
        img = Image.open(tmp_png.name)
        img.save(pdf_path, "PDF", resolution=100.0)
        return pdf_path

with open("../data/1713070761661b62a944c96.pdf", "rb") as f:
    text = pdf_to_text(f.read())
    print(text)

# doc = fitz.open("../data/1713070761661b62a944c96.pdf") # open a document
# out = open("output.txt", "wb") # create a text output
# for page in doc: # iterate the document pages
#     tables = page.find_tables()
#     # out.write(tables)
#     print(*[ tab.to_markdown() for tab in tables.tables])
#     text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
#     out.write(text) # write text of page
#     out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
# out.close()