import streamlit as st
from streamlit_antd_components import MenuItem, menu

def form_entry():
    st.title('Enter Form')
    with st.form(key='my_form'):
        labels = ['Name', 'ID', 'Station Code', 'Crime Category Code', 'Crime Description']
        form_data = {}
        for label in labels:
            form_data[label] = [st.text_input(label=label)]
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
        st.write(f"File uploaded successfully: {uploaded_file.name}")


def info():
    st.title('Register Offender')
    st.write('Select the method to register an offender.')
    st.write('You can either enter the details in the form or upload a document.')
    st.write("Click on the 'Form Entry' or 'Document Upload' option to proceed.")

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