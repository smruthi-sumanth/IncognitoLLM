import tempfile
from ocrmypdf import ocr
from PIL import Image
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar
from pypdf import PdfReader

from frontend.backend.components.anonymize import initialize_analyzer


class OCR:
    def analyze_text(self):
        """
        Analyze the text using the Presidio analyzer engine.

        Returns:
            list: The results of the analysis.
        """
        analyzed_character_sets = []
        analyzer = initialize_analyzer()
        for page_layout in extract_pages("./sample_data/sample.pdf"):
            for text_container in page_layout:
                if isinstance(text_container, LTTextContainer):

                    # The element is a LTTextContainer, containing a paragraph of text.
                    text_to_anonymize = text_container.get_text()

                    # Analyze the text using the analyzer engine
                    analyzer_results = analyzer.analyze(text=text_to_anonymize, language='en')

                    if not text_to_anonymize.isspace():
                        print(text_to_anonymize)
                        print(analyzer_results)

                    characters = list([])

                    # Grab the characters from the PDF
                    for text_line in filter(lambda t: isinstance(t, LTTextLine), text_container):
                        for character in filter(lambda t: isinstance(t, LTChar), text_line):
                            characters.append(character)

                    # Slice out the characters that match the analyzer results.
                    for result in analyzer_results:
                        start = result.start
                        end = result.end
                        analyzed_character_sets.append({"characters": characters[start:end], "result": result})

    def png_to_pdf(self, png_file):
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

    def pdf_to_text(self, pdf_file):
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
                    self.analyze_text()
                    for page in reader.pages:
                        out_text = '\n\n'.join([out_text, page.extract_text()])

            return out_text
