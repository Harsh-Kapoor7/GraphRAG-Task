# Use an official Python runtime as a base image
FROM python:3.10  

# Set the working directory in the container
WORKDIR /app  

# Install system dependencies
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr  

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application code
COPY . .  

# Expose Streamlit port
EXPOSE 8501  

# Run the Streamlit app
CMD ["streamlit", "run", "main.py"]
