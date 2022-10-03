FROM python:3.9

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY . /app

RUN chmod +x ./run_celery.sh

CMD ["flask", "--app", "main", "run", "--host", "0.0.0.0", "--port", "8010"]

