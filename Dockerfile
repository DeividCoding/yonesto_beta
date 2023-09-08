FROM python:3.11.5-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY src/ .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]