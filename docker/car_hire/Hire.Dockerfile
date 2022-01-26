FROM python:3.8

RUN apt-get update

# # Install system dependencies
RUN apt-get install -y software-properties-common \
                       wget \
                       curl \
                       python3-pip \
                       unzip \
                       xvfb

# Download and install firefox
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F
RUN apt-add-repository "deb http://ppa.launchpad.net/ubuntu-mozilla-security/ppa/ubuntu bionic main" -y
RUN apt-get update -y
RUN apt-get install firefox -y

# Download and install geckodriver
RUN GECKODRIVER_VERSION=$(curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+') && \
    wget https://github.com/mozilla/geckodriver/releases/download/"$GECKODRIVER_VERSION"/geckodriver-"$GECKODRIVER_VERSION"-linux64.tar.gz && \
    tar -xvzf geckodriver* && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin

# Add and install dependencies
RUN pip install --no-cache-dir --upgrade pip
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Creates, copies and moves into a new working directory
WORKDIR /Car_Scraper
COPY src/car_hire .

RUN ["chmod", "+x", "./commands.sh"]

CMD ["./commands.sh"]


# -it flag for docker run interactive
# docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=cheapflights -it carhire