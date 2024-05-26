# For Presidio
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# For console output
from pprint import pprint

# For extracting text
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine

# For updating the PDF
from pikepdf import Pdf, AttachedFileSpec, Name, Dictionary, Array


analyzer = AnalyzerEngine()

analyzed_character_sets = []

for page_layout in extract_pages("test.pdf"):
    for text_container in page_layout:
        if isinstance(text_container, LTTextContainer):

            # The element is a LTTextContainer, containing a paragraph of text.
            text_to_anonymize = text_container.get_text()

            # Analyze the text using the analyzer engine
            analyzer_results = analyzer.analyze(text=text_to_anonymize, language='en')

            if text_to_anonymize.isspace() == False:
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


# Combine the bounding boxes into a single bounding box.
def combine_rect(rectA, rectB):
    a, b = rectA, rectB
    startX = min(a[0], b[0])
    startY = min(a[1], b[1])
    endX = max(a[2], b[2])
    endY = max(a[3], b[3])
    return (startX, startY, endX, endY)


analyzed_bounding_boxes = []

# For each character set, combine the bounding boxes into a single bounding box.
for analyzed_character_set in analyzed_character_sets:
    completeBoundingBox = analyzed_character_set["characters"][0].bbox

    for character in analyzed_character_set["characters"]:
        completeBoundingBox = combine_rect(completeBoundingBox, character.bbox)

    analyzed_bounding_boxes.append({"boundingBox": completeBoundingBox, "result": analyzed_character_set["result"]})

pdf = Pdf.open("test.pdf")

annotations = []

# Create a highlight annotation for each bounding box.
for analyzed_bounding_box in analyzed_bounding_boxes:
    boundingBox = analyzed_bounding_box["boundingBox"]

    # Create the annotation.
    # We could also create a redaction annotation if the ongoing workflows supports them.
    highlight = Dictionary(
        Type=Name.Annot,
        Subtype=Name.Highlight,
        QuadPoints=[boundingBox[0], boundingBox[3],
                    boundingBox[2], boundingBox[3],
                    boundingBox[0], boundingBox[1],
                    boundingBox[2], boundingBox[1]],
        Rect=[boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3]],
        C=[1, 0, 0],
        CA=0.5,
        T=analyzed_bounding_box["result"].entity_type,
    )

    annotations.append(highlight)

# Add the annotations to the PDF.
pdf.pages[0].Annots = pdf.make_indirect(annotations)

# And save.
pdf.save("test_annotated.pdf")