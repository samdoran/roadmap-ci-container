FROM registry.access.redhat.com/ubi10-minimal:10.0-1751880071 AS base

FROM base as builder

RUN microdnf -y --nodocs install \
        gcc \
        git \
        libpq-devel \
        make \
        python3.12 \
        python3-devel \
    && microdnf clean all

COPY requirements.txt /usr/share/container-setup/requirements.txt

RUN python -m venv /opt/venvs/ci \
    && /opt/venvs/ci/bin/python -m pip install -U pip \
    && /opt/venvs/ci/bin/python -m pip install --no-cache-dir -r /usr/share/container-setup/requirements.txt


FROM base as final

ENV VENV=/opt/venvs/ci
ENV PATH="${VENV}/bin:$PATH"
ENV PYTHONPATH=/opt/venvs/ci/

COPY --from=builder /opt/venvs/ /opt/venvs/

RUN microdnf install -y --nodocs \
    libpq \
    python3.12 \
    && rm -rf /var/cache/yum/*
