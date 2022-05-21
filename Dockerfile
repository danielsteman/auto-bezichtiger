FROM python:3.10-buster

COPY requirements.txt requirements.txt

RUN apt-get -y update
RUN apt-get install -y unzip xvfb libxi6 libgconf-2-4
RUN apt-get install default-jdk
# Install Chrome dependencies
RUN apt-get install -y wget fonts-liberation
# Download and install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo dpkg -i google-chrome-stable_current_amd64.deb
# Install Python dependencies
RUN pip install -U pip && pip install --user -r requirements.txt

ENV PYTHONPATH="."
ENV PYTHONPATH="/root/.local/bin"

WORKDIR /app
COPY settings.yaml settings.yaml
COPY src src

CMD [ "python", "src/main.py" ]

# https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/