# Infra-toolkit


## What is it?
Is a simple tool for identification of web-services running on your network, and also permits doing a simple heltacheck in those services.

## Requirements
The toolkit can be used in two ways, 
 - 1. Using python.
 - 2. Using Docker.
### Using python
Install dependencies using requirements.txt:
```bash
pip install -r requirements.txt
```
and then run `python main.py` inside the root folder.

### Using Docker
Build the docker image using the dockerfile file:
```bash
docker build -t infra-toolkit .
```
And to run the container:
```bash 
docker run --rm -it infra-toolkit
```