FROM python:3.12-slim

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential && \
    apt-get clean

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"]