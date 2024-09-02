# Use the official Python 3.9 image as the base image
FROM python:3.9

# Install FFMPEG
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY ./src ./src

ENV FLASK_APP=src/main.py

EXPOSE 3000

# Set the command to run the application
CMD [ "flask", "run", "--host=0.0.0.0", "--port=3000" ]