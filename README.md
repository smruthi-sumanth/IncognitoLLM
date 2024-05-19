# SecuraX: Unleashing AI for Smarter Policing with Privacy Baked In 🔒

SecuraX is an AI-powered platform that enables law enforcement agencies to leverage the power of cutting-edge technologies like Zero-Knowledge Proofs, Federated Learning, and Large Language Models (LLMs) while ensuring data privacy and civil liberties.

## Features

- **Zero-Knowledge Proofs**: Analyze data without exposing sensitive information.
- **Federated Learning**: Collaboratively train AI models while keeping data on-premises.
- **Pseudonymization**: Anonymize and mask personal data in documents with flexible retrieval options.
- **Streamlit Frontend**: Intuitive web-based interface for seamless user interaction.

## Getting Started

### Prerequisites

- Python 3.7+
- Poetry (Python package and dependency manager)
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/SecuraX.git
```

2. Navigate to the project directory:

```bash
cd SecuraX
```

3. Install dependencies using Poetry:

```bash
poetry install
```

### Running Locally

1. Start the Streamlit frontend:

```bash
poetry run streamlit run app.py
```

2. Access the application in your web browser at `http://localhost:8501`.

### Running with Docker

1. Build the Docker image:

```bash
docker build -t securax .
```

2. Run the Docker container:

```bash
docker run -p 8501:8501 securax
```

> Note: You can use an already existing version of this image:
```
docker pull p1utoze/securax:v1.0
```

3. Access the application in your web browser at `http://localhost:80`.

## Contributing

We welcome contributions from the community! Please fork the repository, create a new branch, and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the intuitive frontend framework.
- [Poetry](https://python-poetry.org/) for dependency management.
- [Docker](https://www.docker.com/) for containerization.

This README.md provides an overview of the SecuraX project, including its features, installation instructions for local and Docker-based deployment, contribution guidelines, and licensing information. It also acknowledges the key technologies and tools used in the project.
