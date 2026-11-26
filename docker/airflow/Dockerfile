FROM apache/airflow:3.1.3-python3.12

COPY --chown=airflow:root requirements.txt requirements-dev.txt /tmp/

RUN pip install --no-cache-dir \
    -r /tmp/requirements.txt \
    --constraint \
    "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.3/constraints-3.12.txt"

RUN pip install --no-cache-dir \
    "apache-airflow==3.1.3" \
    -r /tmp/requirements-dev.txt

WORKDIR /opt/airflow