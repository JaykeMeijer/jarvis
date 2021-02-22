FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python3-pip libasound2-dev libpulse-dev swig \
    pulseaudio wget tzdata

RUN mkdir /pa
WORKDIR /pa
RUN wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
RUN tar zxf pa_stable_v190600_20161030.tgz
WORKDIR portaudio
RUN ./configure --without-jack
RUN make install
RUN ldconfig

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "listen.py"]