FROM rabbitmq:3.9-management

ARG QUEUE_INTERFACE_PORT

RUN apt-get update -y && apt-get install curl -y

ENV QUEUE_INTERFACE_PORT=${QUEUE_INTERFACE_PORT}

HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 \
    CMD curl -f http://localhost:${QUEUE_INTERFACE_PORT} || exit 1