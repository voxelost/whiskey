FROM python:3.10-bullseye

COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]