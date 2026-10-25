FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Flask uses
EXPOSE 6000

# Default command (overridden by docker-compose)
CMD ["python", "app.py"]
