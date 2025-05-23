FROM python:3.12

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload