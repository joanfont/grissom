FROM library/python:3.6-alpine
MAINTAINER Joan Font <joanfont@gmail.com>

RUN apk add --update build-base \
	libffi-dev \
	libxml2-dev \
	libxslt-dev \
	openssl-dev

WORKDIR /code/

ADD ./ /code/
ARG BUILD_ENV=prod
RUN pip install -r docker/environment/requirements-${BUILD_ENV}.txt


ENTRYPOINT ["python3"]
