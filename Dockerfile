# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Create a non-root user and switch to it
RUN useradd -m aayushi
USER aayushi

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the volume
VOLUME /data

# Run app.py when the container launches
CMD ["python", "app.py"]
