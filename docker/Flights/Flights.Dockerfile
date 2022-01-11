FROM python:3.9.9-buster

RUN apt-get update -y

RUN apt-get install curl \
                    wget \
                    pip3

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 98.0.4758.48
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "https://chromedriver.storage.googleapis.com/index.html?path=${CHROMEDRIVER_VERSION}/"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN pip install --no-cache-dir --upgrade pip
ADD requirements.txt /tmp/requirements
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /Flights_Scraper
COPY src/Flights /Flights_Scraper/