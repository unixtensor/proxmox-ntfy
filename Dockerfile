FROM debian

RUN apt-get update && \
    apt-get install -y lm-sensors python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./src .

ENTRYPOINT [ "python3", "src/main.py" ]