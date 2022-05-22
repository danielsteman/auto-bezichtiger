FROM python:3.10-buster

# Copy Python dependency names and version numbers
COPY requirements.txt requirements.txt
# Install Chrome dependencies
RUN apt-get -y update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libgbm1
# Download and install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
# Install Python dependencies
RUN pip install -U pip && pip install --user -r requirements.txt
# Set wd
WORKDIR /app
# Copy settings and code into wd
COPY settings.yaml settings.yaml
COPY src src

CMD [ "python", "src/main.py" ]