# syntax=docker/dockerfile:1

FROM python:3.9.19-bookworm

RUN \
    pip3 install \
        pyyaml \
        hvac \
        elasticsearch==9.1.3 \
        psutil

WORKDIR /temper

COPY src/ ./src/
COPY conf/ ./conf/
COPY elastic/ ./elastic/
