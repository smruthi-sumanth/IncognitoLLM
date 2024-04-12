import streamlit as st
from newsapi import NewsApiClient
import folium
import geopandas as gpd

newsapi = NewsApiClient(api_key='84b809c2bd574df1a44f4bd6a8c77edd')

# Initialize session state for form submission and document upload
if 'submitted_form' not in st.session_state:
    st.session_state['submitted_form'] = False
if 'uploaded_document' not in st.session_state:
    st.session_state['uploaded_document'] = False

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ["Home", "Enter Form", "Attach Document"])

    if page == "Home":
        st.title('Karnataka State Police')
        st.header("Karnataka State Police")
        show_district_layer = st.checkbox("Show District Layer")
        show_parliamentary_layer = st.checkbox("Show Parliamentary Boundaries Layer")
        display_map(show_district_layer, show_parliamentary_layer)
        st.header("The Times of India.")
        if st.button('Fetch News Updates'):
            display_news_updates()
    elif page == "Enter Form":
        st.title('Enter Form')
        with st.form(key='my_form'):
            name = st.text_input(label='Name')
            ID = st.text_input(label='Enter ID')
            station = st.text_input(label='Station Code')
            crime_category_code=st.text_input(label='Crime Category Code')
            crime_description=st.text_input(label='Provide Description of Crime')
            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                st.session_state['submitted_form'] 
                st.write(f'Submitted Name: {name}')
                st.write(f'Submitted ID: {ID}')
                st.write(f'Submitted Station Code: {station}')
                st.write(f'Submitted Crime Category Code: {crime_category_code}')
                st.write(f'Submitted Crime Description: {crime_description}')
    elif page == "Attach Document":
        st.title('Attach Document')
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
        if uploaded_file is not None:
            st.session_state['uploaded_document'] = True # Set the session state to True
            st.write(f"File uploaded successfully: {uploaded_file.name}")

    # Display the new page based on the session state
    if st.session_state['submitted_form'] or st.session_state['uploaded_document']:
        st.title('AI Recommendations')
        col1, col2 = st.columns(2)
        with col1:
            st.header('Crime details')
        with col2:
            st.header('LLM Retraction Suggestions')


def display_map(show_district_layer, show_parliamentary_layer):
    m = folium.Map(location=[15.3172, 75.7139], zoom_start=6)
    
    m.fit_bounds([[11.5, 73.5], [18.5, 79.5]])
    
    if show_district_layer:
        shapefile_path = 'shapefiles/District.shp'
        gdf = gpd.read_file(shapefile_path)
        
        folium.GeoJson(
            gdf.to_json(),
            style_function=lambda feature: {
                'fillColor': '#FFC0CB',
                'color': '#FFC0CB',
                'weight': 2,
                'fillOpacity': 0.7
            }
        ).add_to(m)
    
    if show_parliamentary_layer:
        shapefile_path = 'shapefiles/PC_Boundary.shp'
        gdf = gpd.read_file(shapefile_path)
        
        folium.GeoJson(
            gdf.to_json(),
            style_function=lambda feature: {
                'fillColor': '#ADD8E6',
                'color': '#ADD8E6',
                'weight': 2,
                'fillOpacity': 0.7
            }
        ).add_to(m)
    map_html = m._repr_html_()
    
   
    st.components.v1.html(map_html, height=600, width=800) 

def display_news_updates():
    top_headlines = newsapi.get_top_headlines(sources='the-times-of-india', language='en')
    for article in top_headlines['articles']:
        st.write(f"{article['title']} - {article['url']}")

if __name__ == "__main__":
    main()
