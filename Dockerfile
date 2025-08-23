# Use a slim Python base image
FROM python:3.13-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN  pip install -r requirements.txt

# Copy the application source code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]