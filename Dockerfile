FROM python:3.7-slim-buster
EXPOSE 5000
EXPOSE 5432
COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt
COPY ./src/ ./src/


WORKDIR ./src
RUN set FLASK_APP start.py
ENV FLASK_APP start.py
CMD ["flask",  "run", "--host=0.0.0.0"]
