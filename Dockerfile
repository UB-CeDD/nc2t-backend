# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]