# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables to prevent Python from writing pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev pkg-config gcc \
    && apt-get clean

# Copy requirements first for caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app/

# To run this container with port mapping, use:
# docker run -p 8000:8000 messaging_app

# Expose the port Django will run on
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
