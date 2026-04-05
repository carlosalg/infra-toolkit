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

The python method generates two json files as reports of the scan and healchecks.

### Using Docker
Build the docker image using the dockerfile file:
```bash
docker build -t infra-toolkit .
```
And to run the container:
```bash 
docker run --rm -it infra-toolkit
```

if you find any problems with the tool no accesing the network, use:
```bash 
docker run --rm -it --network host infra-toolkit
```
In the docker method, for the container to generate the reports files, you need to run the container like this:
```bash
docker run --rm -it --network host -v $(pwd)/reports:/app/reports infra-toolkit
```
what this does is mount a local volume inside the working folder, in where it will be saved the generated files inside the container.

## Usage
When using the toolkit, you will be asked for an CIDR in this format `192.168.1.0/24`, if you are running the toolkit via python, it will also ask for root/sudo password.