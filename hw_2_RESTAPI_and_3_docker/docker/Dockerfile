FROM python:3.12

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    python -m pip install --upgrade pip

WORKDIR /work
ENV PYTHONPATH=/work

COPY . /work/hw_2_RESTAPI_and_3_docker
COPY requirements.txt /work

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080:8080

CMD ["uvicorn", "hw_2_RESTAPI_and_3_docker.main:app", "--port", "8080", "--host", "0.0.0.0"]