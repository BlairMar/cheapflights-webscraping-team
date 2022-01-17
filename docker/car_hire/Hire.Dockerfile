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

# # Download and install Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# RUN ["apt-get", "-y",  "update"]
# RUN ["apt-get", "install",  "-y", "google-chrome-stable"]

# Download and install geckodriver
RUN GECKODRIVER_VERSION=$(curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+') && \
    wget https://github.com/mozilla/geckodriver/releases/download/"$GECKODRIVER_VERSION"/geckodriver-"$GECKODRIVER_VERSION"-linux64.tar.gz && \
    tar -xvzf geckodriver* && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin

# # Download and install chromedriver
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN apt-get install -yqq unzip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# RUN chmod +x /usr/local/bin/chromedriver

# Add and install dependencies
RUN pip install --no-cache-dir --upgrade pip
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# RUN apt-get remove -y curl \
#                       wget \
#                       python3-pip \
#                       software-properties-common

# COPY new_user_credentials.csv .

# Creates, copies and moves into a new working directory
WORKDIR /Car_Scraper
COPY src/car_hire .

# RUN useradd user \
#     && chown -R user /Car_Scraper \
#     && chmod -R u+x /Car_Scraper
# USER user

COPY commands.sh ./Scripts/commands.sh 

RUN ["chmod", "+x", "./Scripts/commands.sh"]

CMD ["./Scripts/commands.sh"]

# -it flag for docker run interactive

# Install firefox
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F && \
#     add-apt-repository ppa:ubuntu-mozilla-daily/ppa && \
#     apt-get update -y && \
#     apt-get install firefox

# ENV firefox_ver 96.0

# RUN curl -fL -o /tmp/firefox.tar.bz2 \
#     https://ftp.mozilla.org/pub/firefox/releases/${firefox_ver}/linux-x86_64/en-GB/firefox-${firefox_ver}.tar.bz2 \
#     && tar -xjf /tmp/firefox.tar.bz2 -C /tmp/ \
#     && mv /tmp/firefox /usr/bin/firefox

# ENV PATH /usr/bin/firefox:$PATH

# Install geckdriver
# RUN GECKODRIVER_VERSION=$(curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+') && \
#     wget https://github.com/mozilla/geckodriver/releases/download/"$GECKODRIVER_VERSION"/geckodriver-"$GECKODRIVER_VERSION"-linux64.tar.gz && \
#     tar -xvzf geckodriver* && \
#     chmod +x geckodriver && \
#     mv geckodriver /usr/local/bin

# ENV geckodriver_ver 0.30.0

# RUN curl -fL -o /tmp/geckodriver.tar.gz \
#     https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_ver}/geckodriver-v${geckodriver_ver}-linux64.tar.gz \
#     && tar -xzf /tmp/geckodriver.tar.gz -C /tmp/ \
#     && chmod +x /tmp/geckodriver \
#     && mv /tmp/geckodriver /usr/local/bin

# docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=cheapflights -it carhire