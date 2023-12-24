FROM python:3.10.13-bookworm

WORKDIR /app
COPY ./src ./src
COPY /requirements.txt /tmp/

RUN pip install -U pip setuptools
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "src/main.py"]
