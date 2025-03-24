# Use a lightweight Python 3.9 image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose port 8000 for the Django development server
EXPOSE 8000

# Command to run the Django server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]