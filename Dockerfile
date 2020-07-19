FROM library/python:3.6-alpine
MAINTAINER Joan Font <joanfont@gmail.com>

RUN apk add --update build-base \
	libffi-dev \
	libxml2-dev \
	libxslt-dev \
	openssl-dev

WORKDIR /code/

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /code/

ENTRYPOINT ["python3"]
