FROM --platform=linux/amd64 python:3.9.9-buster

RUN apt-get update -y

RUN apt-get install -y curl \
                    wget \
                    python3-pip

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >>   /etc/apt/sources.list
# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get -y install google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 98.0.4758.48
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN pip install --no-cache-dir --upgrade pip
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /Flights_Scraper
COPY src/flights /Flights_Scraper/