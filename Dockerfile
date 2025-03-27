# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port for the API
EXPOSE 8000

# Run the deploy script as an example (update command for a production server)
CMD ["python", "scripts/deploy_model.py"]
