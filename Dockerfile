FROM python:3.8-slim

COPY /requirements.txt /api/requirements.txt

ENV APP_DIR='/api'
ENV LOG_LEVEL='info'
ENV DEBUG='FALSE'
ENV UVICORN_EXTRA_FLAGS=''
WORKDIR $APP_DIR

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --compile -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

RUN if [ $DEBUG == 'TRUE' ]; then \
        LOG_LEVEL='debug'; \
    fi

ADD /spaas $APP_DIR/spaas/

EXPOSE 8888

CMD uvicorn spaas:app --host 0.0.0.0 --port 8888 --log-level $LOG_LEVEL --reload