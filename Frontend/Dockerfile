# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app to run on
EXPOSE 5000

# Define environment variables
ENV FLASK_APP app.py
ENV FLASK_ENV development

# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
