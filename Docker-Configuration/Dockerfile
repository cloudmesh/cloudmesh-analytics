FROM ubuntu:19.04

RUN set -x \
        && apt-get -y update \
        && apt-get -y upgrade \
        && apt-get -y --no-install-recommends install build-essential \
                                                      git \
                                                      openssl \
                                                      curl \
                                                      wget \
                                                      sudo \
        && apt-get -y install python3 \
                              python3-pip \ 
        && rm -rf /var/lib/apt/lists/* \
        && update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
        && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 \
        && pip install cloudmesh-installer

RUN mkdir cm
WORKDIR cm

RUN cloudmesh-installer git clone cloud
RUN cloudmesh-installer install cloud -e

# can dockerize python app after this line
# Set the working directory to /ai_services on Docker
WORKDIR /ai_services

# Copy the current directory contents into the container at /ai_services
COPY . /ai_services

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8000 available
EXPOSE 8000

# Run server.py when the container launches
CMD ["python3","server.py"]