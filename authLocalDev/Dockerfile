# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install FFmpeg libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libavfilter-dev libswscale-dev libswresample-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000
EXPOSE 3333
EXPOSE 3334

# Define environment variable
ENV FLASK_ENV=production

# Run app.py when the container launches
CMD ["python3", "app.py"]
