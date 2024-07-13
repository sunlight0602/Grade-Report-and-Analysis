# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run your FastAPI application using Uvicorn
CMD ["./run_main.sh"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]