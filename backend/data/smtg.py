from pypdf import PdfReader, PdfWriter
from presidio_analyzer import AnalyzerEngine
import fitz  # PyMuPDF library


def annotate_pdf_with_entities(pdf_path):
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)

        # Create a new PDF document to hold the annotated pages
        pdf_writer = PdfWriter()

        # Iterate through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            # Open the PDF page using PyMuPDF
            doc = fitz.Document(pdf_path)
            fitz_page = doc[page_num]

            # Annotate the PDF page with the recognized entities
            for entity in analysis:
                # Search for entity text within the page content
                entity_text = entity.content
                matches = fitz_page.search(entity_text, quads=True)  # Get quadrants (bounding boxes) for matches

                # Add highlight annotations for each match
                for quad in matches:
                    annot = fitz_page.add_highlight_annot(quad)
                    annot.update()

            # Add the annotated page to the new PDF document
            pdf_writer.add_page(page)

        # Write the annotated PDF document to a file

        with open("annotated_pdf.pdf", "wb") as output_file:
            pdf_writer.write(output_file)

        # Example usage
        annotate_pdf_with_entities("1713070761661b62a944c96.pdf")
