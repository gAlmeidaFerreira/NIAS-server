FROM rabbitmq:3.9-management

RUN apt-get update -y && apt-get install curl -y

ARG QUEUE_INTERFACE_PORT

HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 \
    CMD curl -f http://localhost:15672 || exit 1