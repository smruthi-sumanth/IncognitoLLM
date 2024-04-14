import io
import PyPDF2
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from backend.components.anonymize import initialize_analyzer
from backend.prompts import TEMPLATE_V1
from backend.utils.schema import FIRDetails


class LLM:
    def __init__(self):
        self.analyzer = initialize_analyzer()
        self.gemini = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, temperature=0.0)
        self.parser = PydanticOutputParser(pydantic_object=FIRDetails)

    def _load_pdf(self, byte_stream) -> str:
        """
        Load the PDF file and extract the text content.

        Args:
            byte_stream (bytes): The byte stream of the PDF file.

        Returns:
            str: The text content of the PDF file.
        """
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(byte_stream))
        page_content = ""
        for page in pdf_reader.pages:
            page_content += page.extract_text()

        return page_content

    def _prompt_generate(self) -> PromptTemplate:
        """
        Generate the prompt for the user.

        Returns:
            PromptTemplate: The prompt template for the user.
        """

        format_instructions = self.parser.get_format_instructions()
        prompt = PromptTemplate(
            template=TEMPLATE_V1,
            suffix="The FIR details are as follows: \n {pdf_content}",
            input_variables=["pdf_content"],
            partial_variables={"format_instructions": format_instructions, "format": "JSON"},
        )

        return prompt

    def process_pdf(self, byte_stream):
        """
        Process the PDF file and extract the FIR details.

        Args:
            byte_stream (bytes): The byte stream of the PDF file.

        Returns:
            list: The results of the analysis.
        """
        pdf_content = self._load_pdf(byte_stream)
        chain = self._prompt_generate() | self.gemini | self.parser
        result = chain.invoke({"pdf_content": pdf_content})

        text = ""
        for key, value in result.dict().items():
            if key in ["accused_details", "victim_details", "stolen_property_details"]:
                if value:
                    for key1, value1 in value[0].items():
                        text += f"{key+'_'+key1}: {value1}\n"
            else:
                text += f"{key}: {value}\n"

        return self.analyzer.analyze(text=text, language="en")