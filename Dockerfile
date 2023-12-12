# Use the official Python 3.12 image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the entire project folder into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 80

# Command to run the application
CMD ["python", "main.py"]