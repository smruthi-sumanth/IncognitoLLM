from langchain_community.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from datetime import datetime
from typing import Optional
from langchain.chains import LLMChain
from typing import List

from backend.components.anonymize import initialize_analyzer
from backend.utils.schema import FIRDetails


def load_pdf():
    loader = PyPDFLoader("test.pdf")
    pages = loader.load()
    result = []
    for page in pages:
        result.append(page.page_content)

    return '\n'.join(result)


TEMPLATE_V1 = """
You are A Police Officer. You have received a First Information Report (FIR) in PDF format.
You must convert the PDF to appropriate format. Stick to the structure of the form.
Do not change the structure of the form. Do not change the values of the form. 

{format_instructions}
"""

parser = PydanticOutputParser(pydantic_object=FIRDetails)
gemini = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, temperature=0.0)

prompt = PromptTemplate(
    template=TEMPLATE_V1,
    suffix="The FIR details are as follows: \n {pdf_content}",
    input_variables=["pdf_content"],
    partial_variables={"format_instructions": parser.get_format_instructions(), "format": "JSON"},
)
analyzer = initialize_analyzer()

pdf_content = load_pdf()
chain = prompt | gemini | parser
result = chain.invoke({"pdf_content": pdf_content})

text = ""
for key, value in result.dict().items():
    if key in ["accused_details", "victim_details", "stolen_property_details"]:
        if value:
            for key1, value1 in value[0].items():
                text += f"{key+'_'+key1}: {value1}\n"
    else:
        text += f"{key}: {value}\n"

response = analyzer.analyze(text=text, language="en")
print(response)
