# Use Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project code
COPY . /app/

# We will run the command via Docker Compose, so we can leave CMD empty or basic
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]