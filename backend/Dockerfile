FROM python:3.12-slim
WORKDIR /service
COPY pyproject.toml .
COPY app app
RUN pip install --no-cache-dir ".[cloud]"
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
