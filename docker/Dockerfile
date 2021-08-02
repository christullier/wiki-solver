FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN MULTIDICT_NO_EXTENSIONS=1 python3 -m pip install multidict
RUN YARL_NO_EXTENSIONS=1 python3 -m pip install yarl
RUN python3 -m pip install -r requirements.txt

COPY . .


CMD ["python3", "sock.py"]
