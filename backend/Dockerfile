FROM ubuntu:latest
LABEL authors="p1utoze"

FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /securax

## Install the Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into the container
COPY . ./backend/

# Expose the Streamlit port
RUN apt-get update && apt-get install -y libgl1-mesa-glx

#CMD ["python", "backend/app.py"]
