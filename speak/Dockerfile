FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python3-pip espeak-ng mbrola mbrola-en1

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY say.py say.py

CMD ["python3", "say.py"]