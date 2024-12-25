# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . /app/

# Expose the port Railway will use
EXPOSE 8080

# Run the bot
CMD ["python", "fb_video_downloader_bot.py"]
