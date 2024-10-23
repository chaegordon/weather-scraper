# Use the official Python image
FROM python:3.11.7@sha256:63bec515ae23ef6b4563d29e547e81c15d80bf41eff5969cb43d034d333b63b8

# Set environment variables for Poetry
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$PATH:/root/.local/bin"

# Set the working directory
WORKDIR /app

# Install dependencies required by Poetry and cron
RUN apt-get update && apt-get install -y cron curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Configure Poetry to create virtual environments in the project directory
RUN poetry config virtualenvs.in-project true

# Install Python dependencies using Poetry
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . /app/

# Add the cron job file
COPY cronjobs /etc/cron.d/my-cron-jobs

# Give execution rights on the cron job file
RUN chmod 0644 /etc/cron.d/my-cron-jobs

# Apply the cron job
RUN crontab /etc/cron.d/my-cron-jobs

# Ensure cron keeps running and logs are tailed
CMD mkdir -p /app/logs && touch /app/logs/cron.log && cron && tail -f /app/logs/cron.log