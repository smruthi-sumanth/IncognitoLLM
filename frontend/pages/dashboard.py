import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Database connection details
DB_USER = 'plutoze'
DB_PASS = 'KSP.azure@2024!'
DB_HOST = 'my-ksp-db.postgres.database.azure.com'
DB_PORT = 5432
DB_NAME = 'crime'

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

RECORDS_PER_PAGE = 100
CURRENT_OFFSET = 0

import plotly.express as px

def fetch_paginated_data(engine, page_number):
    query = f"SELECT final_report_date, COUNT(*) as incidents FROM chargesheets GROUP BY final_report_date"
    df = pd.read_sql(query, engine)
    df['final_report_date'] = pd.to_datetime(df['final_report_date'], errors='coerce')
    df.dropna(subset=['final_report_date'], inplace=True)
    return df

# Fetch and prepare data for visualization
try:
    chargesheet_data = fetch_paginated_data(engine, 1)
    chargesheet_data.sort_values(by='final_report_date', inplace=True)
    
    # Filter the data to focus on the years 2000 - 2050
    chargesheet_data_filtered = chargesheet_data[(chargesheet_data['final_report_date'].dt.year >= 2015) & 
                                                (chargesheet_data['final_report_date'].dt.year <= 2025)]
    
    # Use Plotly Express to generate the line graph
    fig = px.line(chargesheet_data_filtered, x='final_report_date', y='incidents', title='Incidents Over Time',
                  labels={'final_report_date':'Date', 'incidents':'Incidents'},
                  template='plotly_white')  # Customize the appearance as needed
    
    # Display the graph

    st.plotly_chart(fig)
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
st.title('Crime statistics')


# Assuming the rest of your setup code remains unchanged...

def fetch_paginated_data(engine, page_number):
    global CURRENT_OFFSET
    CURRENT_OFFSET += RECORDS_PER_PAGE
    query = f"SELECT * FROM accused_details LIMIT {RECORDS_PER_PAGE} OFFSET {CURRENT_OFFSET}"
    return pd.read_sql(query, engine)

# Fetch and prepare data for visualization
page_number = 1
try:
    accused_data = fetch_paginated_data(engine, page_number)
    
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
        fig_sex_pie.update_layout(title_text='Distribution of Sexes Among the Accused)')
        st.plotly_chart(fig_sex_pie)
        
        # Pie chart for presentState distribution
        present_state_distribution = filtered_data['presentState'].value_counts().reset_index()
        present_state_distribution.columns = ['Present State', 'Count']
        
        fig_present_state_pie = go.Figure(data=[go.Pie(labels=present_state_distribution['Present State'],
                                                       values=present_state_distribution['Count'],
                                                       marker_colors=['lightpurple']*len(present_state_distribution),
                                                       hole=.3)])
        fig_present_state_pie.update_layout(title_text='Distribution of Present States Among the Accused')
        st.plotly_chart(fig_present_state_pie)
        
except Exception as e:
    st.error(f"An error occurred: {str(e)}")


