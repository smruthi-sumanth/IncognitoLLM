FROM python:3.11-slim
LABEL authors="p1utoze"

# Set the working directory in the container
WORKDIR /securax

# Copy the requirements file into the container
COPY frontend/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire frontend directory into the container
COPY frontend/ ./frontend/

# Copy the entire backend directory into the container
COPY backend/ ./backend/

# Expose the Streamlit port
EXPOSE 80

WORKDIR /securax/frontend

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80"]