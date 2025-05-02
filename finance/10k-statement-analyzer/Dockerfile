# Dockerfile
# Use official Python image as a base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

CMD ["streamlit", "run", "frontend.py"]