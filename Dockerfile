FROM python:3.10-slim

# Install Java (required for PySpark) and unzip (for Kaggle datasets)
RUN apt-get update && \
    apt-get install -y default-jre unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire codebase into the container
COPY . .

# Set necessary environment variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV KAGGLE_CONFIG_DIR=/app

# Run the pipeline orchestrator
CMD ["python", "main.py"]
