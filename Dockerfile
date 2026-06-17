FROM python:3.11-slim
WORKDIR /app
RUN pip install --timeout=300 --retries=10 flask mysql-connector-python
COPY app2.py .
COPY templates/ templates/
CMD ["python", "app2.py"]
