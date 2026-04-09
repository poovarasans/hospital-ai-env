FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]