ARG WORKDIR=/skypro/test_task
ARG WHEELDIR=/opt/pip_packages

### build ###
FROM python:3.10.1-alpine3.15 as build

ARG WORKDIR
ARG WHEELDIR

ENV PYTHONUNBUFFERED=1
WORKDIR ${WORKDIR}

RUN apk update \
        && apk --no-cache add \
#			postgresql-dev \
			gcc \
            linux-headers \
			libc-dev
#			unixodbc-dev \
#			wget \
#			build-base

COPY requirements.txt ${WORKDIR}

RUN wget -qc https://bootstrap.pypa.io/get-pip.py \
        && python get-pip.py \
        && pip3 wheel --wheel-dir=${WHEELDIR} -r ${WORKDIR}/requirements.txt

### Final ###
FROM python:3.10.1-alpine3.15

ARG WORKDIR
ARG WHEELDIR

WORKDIR ${WORKDIR}

COPY --from=build ${WHEELDIR} ${WHEELDIR}
COPY --from=build ${WORKDIR}/get-pip.py ${WORKDIR}
COPY test_task/ ${WORKDIR}
COPY requirements.txt ${WORKDIR}
COPY uwsgi.ini ${WORKDIR}

RUN python ${WORKDIR}/get-pip.py \
    && pip install -r ${WORKDIR}/requirements.txt --find-links=${WHEELDIR} \
    && rm -rf .cache/pip

CMD uwsgi --ini uwsgi.ini