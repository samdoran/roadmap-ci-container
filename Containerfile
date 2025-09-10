FROM registry.access.redhat.com/ubi10-minimal:10.0-1755721767

ARG UID=1001

RUN microdnf -y --nodocs install \
        git \
        libpq \
        make \
        python3.12 \
    && microdnf clean all

ADD requirements.txt /usr/share/container-setup/requirements.txt

RUN python -m venv /opt/venvs/ci \
    && /opt/venvs/ci/bin/python -m pip install -U pip \
    && /opt/venvs/ci/bin/python -m pip install --no-cache-dir -r /usr/share/container-setup/requirements.txt \
    && chown -R ${UID} /opt/venvs \
    && chmod -R g+w /opt/venvs

ENV VENV=/opt/venvs/ci
ENV PATH="${VENV}/bin:$PATH"
ENV PYTHONPATH=/opt/venvs/ci/
ENV HOME=/var/lib/ci

RUN useradd --key HOME_MODE=0775 --uid ${UID} --gid 0 --create-home --home-dir "${HOME}" ci

USER ci
WORKDIR $HOME
