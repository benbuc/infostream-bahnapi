FROM python:latest


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
ENV PYTHONPATH=/app
RUN poetry install --no-dev --no-interaction --no-ansi
CMD ["uvicorn", "infostream_bahnapi.main:app", "--host", "0.0.0.0", "--port", "8101"]