# (c) 2021-present Michael Hall
FROM python:3.9.5-buster

ENV LANG C.UTF-8
ENV TZ=etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /bot

WORKDIR /bot

RUN python3.9 -m pip install -r requirements.txt

CMD ["python3.9", "bot.py", "configs/config-docker.toml"]
