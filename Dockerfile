# Pull base image
FROM python:3.12-slim

# Update and install libmagic
RUN apt-get update && \
    apt-get install -y libmagic1 && \
    rm -rf /var/lib/apt/lists/* \

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV_PATH .docker.env

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Copy entrypoint script and grant execution permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# Command to run the application using Daphne
CMD ./entrypoint.sh
