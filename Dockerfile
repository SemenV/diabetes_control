FROM ubuntu:22.04
#FROM python:3.7-slim-buster
EXPOSE 5000
EXPOSE 5432
EXPOSE 5001

RUN apt-get update
RUN apt-get install -y socat
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip




COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt
COPY ./src/ ./src/


WORKDIR ./src
RUN set FLASK_APP start.py
ENV FLASK_APP start.py


CMD sh RUN_two_cmd.sh
#CMD ["socat", "TCP4-LISTEN:5001,reuseaddr,fork" ,"TCP:host.docker.internal:5432"]
#CMD ["flask",  "run", "--host=0.0.0.0"]
