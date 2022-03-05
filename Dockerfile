FROM python:latest

RUN apt-get update && apt-get -y install cron

EXPOSE 8101
WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
ENV PATH="/opt/poetry/bin:/opt/poetry/venv/bin/:${PATH}"

COPY ./pyproject.toml ./poetry.lock README.md /app/
RUN poetry install --no-root --no-dev --no-interaction
RUN pip install virtualenv
COPY ./infostream_bahnapi /app/infostream_bahnapi
COPY ./credentials /app/credentials
ENV PYTHONPATH=/app
RUN poetry install --no-dev --no-interaction --no-ansi

COPY deployment/updater_cron /etc/cron.d/updater_cron
RUN chmod 0644 /etc/cron.d/updater_cron
RUN crontab /etc/cron.d/updater_cron
RUN touch /app/gsheet_dump.log

CMD cron && uvicorn infostream_bahnapi.main:app --host 0.0.0.0 --port 8101
