# (c) 2021-present Michael Hall
FROM ubuntu:20.04 as py_common

RUN apt-get update && \
    apt-get upgrade \
        -qq --no-install-recommends \
        -o Dpkg::Options::=--force-confold \
        -o Dpkg::Options::=--force-confdef && \
    apt-get install \
        -qq --no-install-recommends \
        -o Dpkg::Options::=--force-confdef \
    python3.9 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3.9 -m pip install -U wheel setuptools pip

FROM py_common as build_stage

ENV LANG C.UTF-8
ENV TZ=etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get upgrade \
        -qq --no-install-recommends \
        -o Dpkg::Options::=--force-confold \
        -o Dpkg::Options::=--force-confdef && \
    apt-get install \
        -qq --no-install-recommends \
        -o Dpkg::Options::=--force-confdef \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    libgdbm-dev \
    uuid-dev \
    python3-openssl \
    git \
    libhyperscan5 \
    libhyperscan-dev \
    python3.9-dev \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /wheels

COPY . /bot

WORKDIR /bot

RUN ls /bot
RUN python3.9 -m pip install -r requirements.txt

CMD ["python3.9", "bot.py", "configs/config-docker.toml"]
