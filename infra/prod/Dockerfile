FROM python:3.12.8
WORKDIR /code/
ENV PYTHONFAULTHANDLER=true \
    PYTHONUNBUFFERED=true \
    PIP_NO_CACHE_DIR=true \
    PYTHONDONTWRITEBYTECODE=true \
    PATH="${PATH}:/root/.local/bin/"
RUN python -m pip install pipx && \
    python -m pipx install poetry==2.0.1
COPY . .
RUN poetry install --only main -E prod
