FROM python:3.12-slim

WORKDIR /code

COPY . /code

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [""sh", "-c", "alembic upgrade head && uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
