# Etapa de construcción
FROM python:3.12-alpine AS base
LABEL maintainer="postgres@postgresql.com"
LABEL version="1.0"
LABEL description="Proyecto Django Boliche"
RUN apk --no-cache add bash pango ttf-freefont py3-pip curl

# Etapa de construcción
FROM base AS builder
RUN apk --no-cache add py3-pillow py3-scipy py3-cffi \
  linux-headers autoconf automake libtool gcc cmake python3-dev \
  fortify-headers binutils libffi-dev wget openssl-dev libc-dev \
  g++ make musl-dev pkgconf libpng-dev openblas-dev build-base \
  font-noto terminus-font libffi

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Etapa de producción
FROM base
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
ENV PATH /usr/local/lib/python3.12/site-packages:$PATH
RUN ln -s /usr/share/zoneinfo/America/Cordoba /etc/localtime
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app.wsgi"]
