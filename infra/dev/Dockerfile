FROM python:3.12.8
ARG USER_ID
ARG GROUP_ID
RUN addgroup --gid ${GROUP_ID} appuser && \
    adduser --uid ${USER_ID} --gid ${GROUP_ID} appuser
USER appuser
WORKDIR /code/
ENV PYTHONFAULTHANDLER=true \
    PYTHONUNBUFFERED=true \
    PIP_NO_CACHE_DIR=true \
    PYTHONDONTWRITEBYTECODE=true \
    PATH="${PATH}:/home/appuser/.local/bin/"
RUN python -m pip install pipx && \
    python -m pipx install poetry==2.0.1
COPY pyproject.toml poetry.lock ./
RUN poetry install
