FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Create symlink for python -> python3 compatibility
RUN ln -s /usr/local/bin/python3 /usr/local/bin/python

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]