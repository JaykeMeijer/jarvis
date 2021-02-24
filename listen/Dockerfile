FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3-pip libasound2-dev \
    libpulse-dev swig pulseaudio wget tzdata libportaudiocpp0 \
    alsa-base alsa-utils git

# RUN mkdir /pa
# WORKDIR /pa
# RUN wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
# RUN tar zxf pa_stable_v190600_20161030.tgz
# WORKDIR portaudio
# RUN ./configure --without-jack
# RUN make install
# RUN ldconfig

RUN git clone -b alsapatch https://github.com/gglockner/portaudio
WORKDIR portaudio
RUN ./configure && make
RUN make install
RUN ldconfig

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "listen.py"]