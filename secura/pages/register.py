import streamlit as st
from streamlit_antd_components import MenuItem, menu
from annotated_text import annotated_text
from settings.helpers import (
    text_analyze, anonymize,
    pdf_to_text,
    annotate,
    replace_markdown_tables_with_csv,
    convert_markdown_to_plain_text,
    redact_encrypted_text
)
from streamlit_extras.stylable_container import stylable_container
from settings.config import FIRDetails, COMPLAINT_DICT, FLAIR_ENTITIES, __KEY, CONTAINER_CSS
from presidio_anonymizer.operators.encrypt import Encrypt
from presidio_anonymizer.operators.decrypt import Decrypt


def form_menu(form):
    form_data = {}

    for label in COMPLAINT_DICT.keys():
        form_data[label] = [form.text_input(label=COMPLAINT_DICT[label])]
        form_data[label].append(form.checkbox(label='is anonymized?', value=True, key=label.lower()))

    submit_button = form.form_submit_button(label='Submit', use_container_width=True)
    return form_data, submit_button


def form_entry():
    st.title('Enter Form')
    st.info('Fill in the details of the offender in the form below.')
    st.warning("Scroll down to see more form fields.")
    # print(scheme)
    button, height = None, 600
    col1, col2 = st.columns(2)
    with col1.container(height=height):
        form = st.form(key='my_form')
        # TODO: INPUT RECEIVED FORM DATA
        data, button = form_menu(form)
    if button:
        scheme = FIRDetails.schema()['properties']
        labels = scheme.keys()
        with col2:
            st.session_state['submitted_form'] = True
            encrypted_data, decrypted_data = {}, {}
            for label in labels:

                try:
                    entry = data[label][0]
                    if not entry or not data[label][1]: continue
                    encrypted_data[label] = (
                        st.session_state["encrypt_class"].operate(entry, {"key": __KEY})
                    )
                    decrypted_data[label] = st.session_state["decrypt_class"].operate(
                        encrypted_data[label], {"key": __KEY}
                    )
                except KeyError:
                    pass

            del entry
            with stylable_container(
                    key="row1",
                    css_styles=CONTAINER_CSS.format(
                        background_color="#C9A503",
                        value="none",
                        height=(height - 10)/2
                    )
            ):
                st.header(":black[ENCRYPTED REDACTED DATA]")
                for field in encrypted_data:
                    st.write(f"**{field}**: {encrypted_data[field]}")
            with stylable_container(
                    key="row2",
                    css_styles=CONTAINER_CSS.format(
                        background_color="#70FF91",
                        value="none",
                        height=(height - 10)/2
                    )
            ):
                st.header(":black[DECRYPTED DATA]")
                for field in decrypted_data:
                    st.write(f"**{field}**: {redact_encrypted_text(decrypted_data[field])}")



def upload_document():
    st.title('Attach Document')
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.session_state['uploaded_document'] = True  # Set the session state to True
        text_data, display_data = pdf_to_text(uploaded_file.read())
        # print(text_data)
        col1, col2 = st.columns([1, 1])
        with col1:
            with st.container(height=600, border=2):
                st.title(f"🗒️:green[PARSED PDF DATA from {uploaded_file.name}]")
                st.markdown(display_data, unsafe_allow_html=True)
        with col2:
            with st.container(height=600, border=2):
                with st.spinner("Analyzing the text data..."):
                    # TODO: ANALYZED TEXT DATA RESULTS
                    analysis_results = text_analyze(text_data, entities=FLAIR_ENTITIES, score_threshold=0.09)
                    if analysis_results:
                        st.title(f"🗒️:green[ANONYMIZED PDF DATA from {uploaded_file.name}]")
                        # print(anonymize(text_data, "mask", analysis_results, mask_char="X", number_of_chars=4).items)
                        results = annotate(text_data, analyze_results=analysis_results)
                        text_data = replace_markdown_tables_with_csv(text_data)
                        text_data = convert_markdown_to_plain_text(text_data)
                        # TODO: Store text data into the database
                        annotated_text(*results)

        # data = st.session_state["llm"].process_pdf(uploaded_file.read())
        st.write(f"File uploaded successfully: {uploaded_file.name}")


def info():
    registration_docs = """
    # Register Offender's Details (FIR) 
    The registration of an offender is a crucial step in the criminal justice process. To perform the process onf SecureX follow the belwo steps:
    
    ### Choose the suitable method:
    - **Form Entry**: Enter the details of the offender in the form provided. It requires you to add in the belwo details:  
        1. Name
        2. Father's/Husband's Name 
        3. Age  
        4. Occupation
        5. Religion
        6. Address
        7. Caste
        8. Phone Number
        9. Date of Issue of FIR
        10. Date of FIR
        11. Address
        12. Sex \n
    - **Document Upload**: Upload a document containing the details of the offender. In this case the document should be 
     in the format of PDF, DOCX or TXT which is the FIR document. 
     """

    st.markdown(registration_docs)


def run():
    if 'register_menu' not in st.session_state:
        st.session_state['register_menu'] = {
            0: info,
            2: form_entry,
            3: upload_document,
        }
    if 'submitted_form' not in st.session_state:
        st.session_state['submitted_form'] = False

    if "register_type" not in st.session_state:
        st.session_state["register_type"] = "form"

    if 'uploaded_document' not in st.session_state:
        st.session_state['uploaded_document'] = False

    if "encrypt_class" not in st.session_state:
        st.session_state["encrypt_class"] = Encrypt()

    if "decrypt_class" not in st.session_state:
        st.session_state["decrypt_class"] = Decrypt()

    layout = st.empty()
    sidebar_width = 0.15
    col1, col2 = layout.columns([sidebar_width, 1 - sidebar_width])
    with col1:
        choice = menu(
            [
                MenuItem('Report Menu', disabled=True),
                MenuItem(type='divider'),
                MenuItem('Form Entry', icon='ui-checks'),
                MenuItem('Document Upload', icon='upload'),
            ],
            variant='filled',
            size='lg',
            color='teal',
            index=0,
            indent=0,
            return_index=True,
        )
        # st.write(f"Selected: {choice}")
    with col2:
        st.session_state['register_menu'][choice]()


if __name__ == "__main__":
    run()
