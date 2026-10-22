FROM python:3.13-slim
RUN useradd --create-home --uid 10001 sandbox
WORKDIR /app
COPY sandbox/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sandbox/worker.py .
USER sandbox
ENTRYPOINT ["python", "worker.py"]
