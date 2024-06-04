FROM python:3.11-slim
LABEL authors="p1utoze"

# Set the working directory in the container
WORKDIR /securax

# Copy the requirements file into the container
COPY secura/requirements.txt .

RUN apt-get update &&  \
    apt-get install libpq-dev python3-dev gcc g++ -y

## Install the Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/securax

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

ARG ENV_CONFIG

# Allow installing dev dependencies in "dev" environment to run tests and lint
RUN bash -c "if [ $ENV_CONFIG == 'dev' ] ; then poetry install --no-root ; else poetry install --no-root --without dev ; fi"


# Copy the entire secura directory into the container
COPY secura/ ./frontend/

# Copy the entire backend directory into the container
COPY secura/backend/ ./backend/

# Expose the Streamlit port
EXPOSE 80

WORKDIR /securax/frontend

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80"]