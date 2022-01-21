FROM --platform=linux/amd64 python:3.8

RUN apt-get update -y

RUN apt-get install -y  curl \
                    wget \
                    python3-pip \
                    software-properties-common \
                    xvfb


# RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe restricted multiverse" && apt-get upgrade -y

# RUN apt --fix-broken install

# RUN apt-get install -y libgconf2-4 libnss3-1d libxss1


# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >>   /etc/apt/sources.list.d/chrome.source.list
# # Update the package list and install chrome
# # RUN apt-get update -y
# # RUN apt-get -y install google-chrome-stable
# # RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
# #     dpkg -i google-chrome-stable_current_amd64.deb
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /usr/bin/ \ 
#                         && apt-get install -y /usr/bin/google-chrome-stable_current_amd64.deb

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN ["apt-get", "-y",  "update"]
RUN ["apt-get", "install",  "-y", "google-chrome-stable"]

# RUN apt-get install -y chromium


# Set up Chromedriver Environment variables
# ENV CHROMEDRIVER_VERSION 98.0.4758.48
# ENV CHROMEDRIVER_DIR /chromedriver
# RUN mkdir $CHROMEDRIVER_DIR

# # Download and install Chromedriver
# RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
# RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# # Put Chromedriver into the PATH
# ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/97.0.4692.71/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/
RUN chmod +x /usr/bin/chromedriver

RUN pip install --no-cache-dir --upgrade pip
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /Flights
COPY src/flights /Flights
COPY src/run_in_docker.sh /Flights/run_in_docker.sh

RUN mkdir /tmp/.X11-unix/

RUN useradd User \
    && chown -R User /Flights \
    && chmod -R u+x /Flights \
    && chmod -R 1777 /tmp/.X11-unix/
USER User

CMD ["bash", "run_in_docker.sh"]