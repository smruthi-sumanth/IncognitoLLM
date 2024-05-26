import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Database connection details
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

# URL encoding the password
encoded_db_pass = quote_plus(DB_PASS)

# SSL certificate path
SSL_CERT_PATH = r'C:\Users\User\AppData\Local\Programs\Python\Python311\Lib\site-packages\certifi\cacert.pem'

# Check if SSL certificate file exists
if not os.path.exists(SSL_CERT_PATH):
    st.error("SSL Certificate File Not Found.")
    raise FileNotFoundError("SSL Certificate File Not Found.")

# Creating the database engine
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{encoded_db_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    connect_args={
        'sslmode': 'require',
        'sslrootcert': SSL_CERT_PATH,
        'connect_timeout': 50
    }
)

def fetch_all_accused_details(engine):
    query = "SELECT * FROM accused_details"
    return pd.read_sql(query, engine)

def display_crime_statistics():
    try:
        # Fetch all accused details
        chargesheet_data = fetch_all_accused_details(engine)
        
        # Ensure 'final_report_date' and 'incidents' columns exist
        if 'final_report_date' not in chargesheet_data.columns or 'incidents' not in chargesheet_data.columns:
            st.error("Required columns ('final_report_date', 'incidents') not found in the dataset.")
            return
        
        # Convert 'final_report_date' to datetime for sorting and filtering
        chargesheet_data['final_report_date'] = pd.to_datetime(chargesheet_data['final_report_date'])
        
        # Sort the data by 'final_report_date'
        chargesheet_data.sort_values(by='final_report_date', inplace=True)
        
        # Filter the data to focus on the years 2015 - 2025
        chargesheet_data_filtered = chargesheet_data[(chargesheet_data['final_report_date'].dt.year >= 2015) & 
                                                    (chargesheet_data['final_report_date'].dt.year <= 2025)]
        
        # Use Plotly Express to generate the line graph
        fig = px.line(chargesheet_data_filtered, x='final_report_date', y='incidents', title='Incidents Over Time',
                      labels={'final_report_date':'Date', 'incidents':'Incidents'},
                      template='plotly_white')  # Customize the appearance as needed
        
        # Display the graph
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

def display_accused_details():
    try:
        # Fetch all accused details
        accused_data = fetch_all_accused_details(engine)
        
        # Filtering data based on age
        filtered_data = accused_data[(accused_data['age'] >= 20) & (accused_data['age'] <= 60)]
        
        # Button to toggle visualization type
        show_bar_chart = st.button('Bar Charts')
        show_pie_chart = st.button('Pie Charts')
        
        # Display bar charts by default
        if not show_pie_chart or show_bar_chart:
            # Bar chart for age distribution
            age_distribution = filtered_data['age'].value_counts().reset_index()
            age_distribution.columns = ['Age Group', 'Number of Accused']
            
            fig_age = go.Figure(data=[go.Bar(x=age_distribution['Age Group'], y=age_distribution['Number of Accused'],
                                              marker_color='blue')])
            fig_age.update_layout(title_text='Distribution of Ages Among the Accused', xaxis_title='Age Group',
                                  yaxis_title='Number of Accused')
            st.plotly_chart(fig_age)
            
            # Bar chart for sex distribution
            sex_distribution = filtered_data['sex'].value_counts().reset_index()
            sex_distribution.columns = ['Sex', 'Count']
            
            fig_sex = go.Figure(data=[go.Bar(x=sex_distribution['Sex'], y=sex_distribution['Count'],
                                               marker_color='blue')])
            fig_sex.update_layout(title_text='Distribution of Sexes Among the Accused', xaxis_title='Sex',
                                yaxis_title='Count')
            st.plotly_chart(fig_sex)
            
            # Bar chart for presentState distribution
            present_state_distribution = filtered_data['presentState'].value_counts().reset_index()
            present_state_distribution.columns = ['Present State', 'Count']
            
            fig_present_state = go.Figure(data=[go.Bar(x=present_state_distribution['Present State'],
                                                y=present_state_distribution['Count'],
                                                marker_color='blue')])
            fig_present_state.update_layout(title_text='Distribution of Present States Among the Accused',
                                       xaxis_title='Present State', yaxis_title='Count')
            st.plotly_chart(fig_present_state)
                
        else:
            # Pie chart for age distribution
            age_distribution = filtered_data['age'].value_counts().reset_index()
            age_distribution.columns = ['Age Group', 'Number of Accused']
            
            fig_age_pie = go.Figure(data=[go.Pie(labels=age_distribution['Age Group'], values=age_distribution['Number of Accused'],
                                           marker_colors=['lightblue']*len(age_distribution),
                                           hole=.3)])
            fig_age_pie.update_layout(title_text='Distribution of Ages Among the Accused')
            st.plotly_chart(fig_age_pie)
            
            # Pie chart for sex distribution
            sex_distribution = filtered_data['sex'].value_counts().reset_index()
            sex_distribution.columns = ['Sex', 'Count']
            
            fig_sex_pie = go.Figure(data=[go.Pie(labels=sex_distribution['Sex'], values=sex_distribution['Count'],
                                    marker_colors=['lightgreen']*len(sex_distribution),
                                    hole=.3)])
            fig_sex_pie.update_layout(title_text='Distribution of Sexes Among the Accused')
            st.plotly_chart(fig_sex_pie)
            
            # Pie chart for state distribution
            state_distribution = filtered_data['state'].value_counts().reset_index()
            state_distribution.columns = ['State', 'Count']
            
            fig_state_pie = go.Figure(data=[go.Pie(labels=state_distribution['State'], values=state_distribution['Count'],
                                      marker_colors=['skyblue']*len(state_distribution),
                                      hole=.3)])
            fig_state_pie.update_layout(title_text='Distribution of States Among the Accused')
            st.plotly_chart(fig_state_pie)
                    
    except Exception as e:
        st.error(f"An error: {str(e)}")

def run():
    st.title('Crime Data Analysis Dashboard')
    st.subheader('Analyze, Secure, and Anonymize (ASA) your data.')
    
    # Display crime statistics
    display_crime_statistics()
    
    # Display accused details
    display_accused_details()

if __name__ == "__main__":
    run()
