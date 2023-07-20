FROM python:3.10-bullseye

COPY . ./
RUN apt install libffi-dev libnacl-dev python3-dev libopus

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]