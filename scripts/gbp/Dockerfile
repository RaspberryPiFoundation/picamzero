FROM debian:bookworm

# COPY build-config.sh /etc/pbuilder/

RUN echo "deb http://deb.debian.org/debian bookworm main" >> /etc/apt/sources.list
RUN echo "deb http://deb.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list
RUN rm /etc/apt/sources.list.d/debian.sources

RUN apt-get update && apt-get install -y wget && \
  cd /etc/apt/trusted.gpg.d/ && wget https://github.com/RPi-Distro/pi-gen/raw/refs/heads/master/stage0/files/raspberrypi.gpg

RUN echo "deb http://archive.raspberrypi.com/debian/ bookworm main" >> /etc/apt/sources.list.d/raspi.list
# ADD https://github.com/RPi-Distro/pi-gen/raw/refs/heads/master/stage0/files/raspberrypi.gpg /etc/apt/trusted.gpg.d/raspberrypi.gpg

RUN apt-get update && apt-get install -y git-buildpackage gnupg

# Build dependencies
RUN apt-get update && apt-get install -y dh-sequence-python3 python3-setuptools python3-all pybuild-plugin-pyproject python3-hatchling python3-opencv python3-picamera2 python3-libcamera

