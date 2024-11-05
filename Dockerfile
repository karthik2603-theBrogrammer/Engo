# Use an official Python runtime as a base image
FROM python:3.11-alpine

# Set up environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set the environment variables
ENV FLASK_APP=main.py

# Expose the port Flask runs on
EXPOSE 5555

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5555"]
