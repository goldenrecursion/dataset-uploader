# Dockerfile

# Official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the source code to the working directory
COPY src/ .

# Copy secrets (Moralis API key and Django Secret Key) to working directory
COPY moralis_api_key.json .
COPY secret_key.txt .

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install required dependencies
RUN pip install -r requirements.txt

# Using port 8000 
EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]