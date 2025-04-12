# Use the official Python image
FROM python:3.9
# Set the working directory
WORKDIR /app
# Copy the project requirements and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt; mkdir -p /app/data
# Copy all project files into the container
COPY . /app/
# Expose the application port
EXPOSE 8080
# Command to run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]