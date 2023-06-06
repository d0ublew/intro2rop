FROM ubuntu@sha256:ca5534a51dd04bbcebe9b23ba05f389466cf0c190f1f8f182d7eea92a9671d00 AS app
# FROM ubuntu@sha256:b795f8e0caaaacad9859a9a38fe1c78154f8301fdaf0872eaf1520d66d9c0b98 AS app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc make
COPY ./chall.c /app/
COPY ./Makefile /app/
COPY ./flag.txt /app/
WORKDIR /app
RUN make

FROM pwn.red/jail
COPY --from=app / /srv
ENV JAIL_MEM=30M JAIL_TIME=300
