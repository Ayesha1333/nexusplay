FROM python:3.11-slim

WORKDIR /app

# Copy the rest of the app
COPY . .

# Expose the port Flask uses
EXPOSE 7000

# Default command (overridden by docker-compose)
CMD ["python", "app.py"]
