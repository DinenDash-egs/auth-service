    # Use an official Python runtime as a base image
    FROM python:3.9

    # Set the working directory in the container
    WORKDIR /app

    # Copy the requirements file
    COPY requirements.txt /app/requirements.txt

    # Install dependencies
    RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

    # Copy application files
    COPY . /app

    # Copy environment variables file
    COPY .env /app/.env

    # Start FastAPI service on port 8001
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
