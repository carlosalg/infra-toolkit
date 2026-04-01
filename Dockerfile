#Base image
FROM python:3.14.3-slim-trixie

LABEL maintainer="Carlos carloos15lcc@gmail.com"
LABEL version="1.0"
LABEL description="Toolkit for infrastructure"
LABEL org.opencontainers.image.source="https://github.com/carlosalg/infra-toolkit"

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends nmap && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
CMD ["python", "main.py"]