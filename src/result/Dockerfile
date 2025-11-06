FROM python:3.12-slim

WORKDIR /app

# Copy the app code and requirements
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default Flask port
EXPOSE 80

# Start the Flask app
CMD ["python", "app.py"]