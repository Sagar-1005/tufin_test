FROM python:3.10-slim

RUN useradd -m tufin

WORKDIR /home/tufin

COPY process_data.py .

RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    rm -rf /var/lib.apt/lists/*

USER tufin

ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "python" , "process_data.py" ]

CMD ["--help"]