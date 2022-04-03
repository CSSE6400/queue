FROM python:3.9

WORKDIR /app

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pip install pipenv && pipenv sync

COPY . .

ENTRYPOINT [ "pipenv", "run", "python", "/app/main.py" ]