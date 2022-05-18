FROM python:3.10-buster

COPY requirements.txt requirements.txt

RUN apt-get -y update
RUN apt-get install -y unzip xvfb libxi6 libgconf-2-4
RUN apt-get install default-jdk
RUN pip install -U pip && pip install --user -r requirements.txt

ENV PYTHONPATH="."
ENV PYTHONPATH="/root/.local/bin"

WORKDIR /app
COPY settings.yaml settings.yaml
COPY src src

CMD [ "python", "src/main.py" ]

# https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/