FROM python:3.12

WORKDIR /app

COPY web_server.py /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1234

CMD ["uvicorn", "web_server:app", "--host", "0.0.0.0", "--port", "1234"]