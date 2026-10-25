FROM python:3.14-slim as build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV path= "/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.14-slim as production
WORKDIR /app
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser
COPY --from=build /opt/venv /opt/venv/
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["python", "app.py"]
