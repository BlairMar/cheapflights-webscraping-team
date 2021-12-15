FROM python:3.8.5

RUN apt-get update -y

# Install system dependencies
RUN apt-install -y curl \
                   wget

# Python dependencies
# RUN apt-install -y python3 

# Install geckodriver and firefox
RUN wget GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xvzf geckodriver* && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin

RUN add-apt-repository ppa:ubuntu-mozilla-daily/ppa && \
    apt-get update -y && \
    apt-get install -y firefox

# Add and install dependencies
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

CMD ["python3", "-u", "CarHireScraper.py"]