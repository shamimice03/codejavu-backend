FROM python:3.10-slim

# Incorporates former base image setup from https://github.com/tiangolo/uvicorn-gunicorn-docker
RUN apt-get update
RUN apt-get -qq -y install curl
RUN apt-get -y install pip


RUN pip install --no-cache-dir uvicorn[standard]==0.18.3
RUN pip install --no-cache-dir gunicorn==20.1.0

EXPOSE 80

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3
ENV PATH="/opt/poetry/bin:$PATH"
#RUN export PATH="/opt/poetry/bin:$PATH"
RUN /opt/poetry/bin/poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./src/pyproject.toml ./src/poetry.lock* /src/

WORKDIR /src/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then /opt/poetry/bin/poetry install --no-root ; else /opt/poetry/bin/poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./src /src
ENV PYTHONPATH=/src

CMD ["/start.sh"]