# syntax=docker/dockerfile:1

FROM python:3.9.19-bookworm

RUN \
    pip install \
        psutil \
        hvac \
        elasticsearch==8.13.0

WORKDIR /temper

COPY src/ ./src/
