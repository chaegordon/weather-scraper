# Description: Dockerfile for the Tomorrow application

# Use the official Python image
FROM python:3.11.7@sha256:63bec515ae23ef6b4563d29e547e81c15d80bf41eff5969cb43d034d333b63b8

# Set the working directory
WORKDIR /app

# Set environment variables, so that the virtual environment is created in the project directory
ENV PATH="/app/.venv/bin:$PATH"

# Disable pip version check
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
# Print logs immediately
ENV PYTHONUNBUFFERED=1
# Disable writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# install poetry
RUN pip install poetry

# Configure Poetry to create virtual environments in the project directory
RUN poetry config virtualenvs.in-project true

# Copy project dependencies
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install dependencies
RUN poetry install

# Copy the application code
COPY ./tomorrow /app/tomorrow

# Copy the test files
COPY ./tests /app/tests
