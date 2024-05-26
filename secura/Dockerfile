FROM ubuntu:latest
LABEL authors="p1utoze"

FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /securax

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire secura directory into the container
COPY . ./frontend/

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
#ENTRYPOINT ["streamlit", "run"]