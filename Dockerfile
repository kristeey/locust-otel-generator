# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Locust
RUN pip install --upgrade pip
RUN pip install locust

# Copy the rest of the application code into the container
COPY . .

# Expose the Locust web interface port
EXPOSE 8089

# Command to run Locust
CMD ["locust", "--config=locust.conf"]