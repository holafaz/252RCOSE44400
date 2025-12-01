FROM python:3.11-slim
WORKDIR /app
COPY app_backend.py .
RUN pip install flask
EXPOSE 5001
CMD ["python", "app_backend.py"]

