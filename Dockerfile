FROM debian

RUN apt-get update && \
    apt-get install -y lm-sensors python3 python3-requests && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

ENTRYPOINT [ "python3", "/src/main.py" ]