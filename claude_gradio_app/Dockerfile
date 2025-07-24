FROM ubuntu:24.04

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

RUN apt-get update
RUN apt-get -yq install wget git tzdata
RUN apt-get -yq install python3.12-dev python3-pip
RUN apt-get upgrade -y
RUN apt-get clean

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN ln -s /usr/bin/python3.12 /usr/bin/python

RUN pip install --break-system-packages --no-cache-dir gradio==4.44.1
RUN pip install --break-system-packages --no-cache-dir pydantic==2.10.6
RUN pip install --break-system-packages --no-cache-dir boto3==1.37.33

WORKDIR /workdir
COPY ./work .
EXPOSE 8080

CMD ["python", "./pgm/front_ui.py"]