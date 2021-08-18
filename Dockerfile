FROM ubuntu:trusty

WORKDIR /junkins
ENV config=config.json
ENV secret=TOP_SECRET
EXPOSE 8083
COPY . .