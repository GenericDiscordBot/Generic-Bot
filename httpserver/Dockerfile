FROM python:3.9.5-buster

ENV LANG C.UTF-8
ENV TZ=etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./httpserver /http
COPY ./configs /http/configs

WORKDIR /http

RUN python3.9 -m pip install -r requirements.txt

EXPOSE 8080

CMD ["python3.9", "./server.py", "configs/config-docker.toml"]
