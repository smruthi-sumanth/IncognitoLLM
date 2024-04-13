import streamlit as st
from newsapi import NewsApiClient
import folium
import geopandas as gpd
from settings.config import SHAPEFILES_DIR
from streamlit_extras.stylable_container import stylable_container
newsapi = NewsApiClient(api_key='84b809c2bd574df1a44f4bd6a8c77edd')

# Initialize session state for form submission and document upload
if 'submitted_form' not in st.session_state:
    st.session_state['submitted_form'] = False
if 'uploaded_document' not in st.session_state:
    st.session_state['uploaded_document'] = False


def display_map(show_district_layer, show_parliamentary_layer, height=500):
    m = folium.Map(location=[15.3172, 75.7139], zoom_start=6)

    m.fit_bounds([[11.5, 73.5], [18.5, 79.5]])

    if show_district_layer:
        shapefile_path = SHAPEFILES_DIR / 'District.shp'
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
        shapefile_path = SHAPEFILES_DIR / 'PC_Boundary.shp'
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

    st.components.v1.html(map_html, height=height)


def display_news_updates():
    top_headlines = newsapi.get_top_headlines(sources='the-times-of-india, the-hindu', language='en')
    with stylable_container(
            key="container_with_border",
            css_styles="""
            {
                background-color: #096A4A;
                color: black;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid black;
                overflow: scroll;
            }
            a {
                color: black;
            }
            """,
    ):
        for article in top_headlines['articles']:
            st.markdown(f"""
            > **{article['title']}** \n\n > Source: [{article['url']}]({article['url']})
            """)
            st.divider()

def run():
    # st.sidebar.title('Navigation')
    # page = st.sidebar.radio("Go to", ["Home", "Enter Form", "Attach Document"])
    st.title('Karnataka State Police')
    st.header('Welcome to the Karnataka State Police Portal')
    st.write('This portal provides information on crime statistics, news updates, and AI recommendations.')
    cols = st.columns([2, 1])
    with cols[0]:
        with st.container(height=800):
            show_district_layer = st.checkbox("Show District Layer")
            show_parliamentary_layer = st.checkbox("Show Parliamentary Boundaries Layer")
            display_map(show_district_layer, show_parliamentary_layer, height=600)
            st.header("The Times of India.")
    with cols[1]:
        with st.container(height=800):
            display_news_updates()

    #
    # # Display the new page based on the session state
    # if st.session_state['submitted_form'] or st.session_state['uploaded_document']:
    #     st.title('AI Recommendations')
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.header('Crime details')
    #     with col2:
    #         st.header('LLM Retraction Suggestions')

