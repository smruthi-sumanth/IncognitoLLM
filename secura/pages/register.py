import streamlit as st
from streamlit_antd_components import MenuItem, menu
from settings.helpers import text_analyze, anonymize, pdf_to_text
from settings.config import FIRDetails, COMPLAINT_DICT
from backend.components.llm import LLM


def form_entry():
    st.title('Enter Form')
    scheme = FIRDetails.schema()['properties']
    labels = scheme.keys()
    # print(scheme)
    with st.form(key='my_form'):
        form_data = {}

        for label in COMPLAINT_DICT.keys():
            form_data[label] = [st.text_input(label=COMPLAINT_DICT[label])]
            form_data[label].append(st.checkbox(label='is anonymized?', value=True, key=label.lower()))

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            for label in labels:
                st.write(f'Submitted {label}: {form_data[label][0]}')


def upload_document():
    st.title('Attach Document')
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.session_state['uploaded_document'] = True  # Set the session state to True
        text_data, display_data = pdf_to_text(uploaded_file.read())
        col1, col2 = st.columns([1, 1])
        with col1:
            with st.container(height=600, border=2):
                st.title(f"🗒️:green[PARSED PDF DATA from {uploaded_file.name}]")
                st.markdown(display_data, unsafe_allow_html=True)
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

    layout = st.empty()
    col1, col2 = layout.columns([0.15, 0.85])
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
