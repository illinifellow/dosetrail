FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY dosetrail ./dosetrail
RUN pip install --no-cache-dir .
COPY drl.yaml sql ./
EXPOSE 11112 8000
CMD ["dosetrail-scp"]