FROM python:3.9.5

WORKDIR /Hotels_Scraper
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src/Hotels ./Hotels_Scraper

RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

COPY src/Hotels/commands.sh ./Scripts/commands.sh 

RUN ["chmod", "+x", "./Scripts/commands.sh"]

CMD ["./Scripts/commands.sh"]



