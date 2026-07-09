# syntax=docker/dockerfile:1

FROM python:3.9.19-bookworm

RUN \
    pip3 install \
        psutil \
        hvac \
        elasticsearch==9.3.3

WORKDIR /temper

COPY src/ ./src/
