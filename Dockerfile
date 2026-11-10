FROM mambaorg/micromamba:2

ENV PYTHONUNBUFFERED=1

# Build the conda environment (named "aics", installed into the image's base env).
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install --yes --name base --file /tmp/environment.yml \
    && micromamba clean --all --yes

WORKDIR /app
COPY app ./app

# The micromamba entrypoint activates the environment, so python and uvicorn are on PATH.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
