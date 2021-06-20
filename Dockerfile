# Docker file ideas taken from https://martinheinz.dev/blog/17

FROM python:3.9-slim-buster AS builder

RUN apt-get update && apt-get install -y --no-install-recommends --yes python3-venv && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install wheel

RUN apt-get install -y --no-install-recommends --yes make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Adding some of the Dockerfile best practices https://github.com/hexops/dockerfile

# Non-root user for security purposes.
#
# UIDs below 10,000 are a security risk, as a container breakout could result
# in the container being ran as a more privileged user on the host kernel with
# the same UID.
#
# Static GID/UID is also useful for chown'ing files outside the container where
# such a user does not exist.
RUN addgroup --gid 10001 --system nonroot \
 && adduser  --uid 10000 --system --ingroup nonroot --home /home/nonroot nonroot


FROM builder AS builder-venv

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt

FROM builder-venv AS runner

COPY --from=builder-venv /venv /venv
COPY . ./app
WORKDIR /app

# Use the non-root user to run our application
USER nonroot

EXPOSE 8080

CMD ["/venv/bin/python", "-m", "uvicorn", "setup:app", "--host", "0.0.0.0", "--port", "8080"]
