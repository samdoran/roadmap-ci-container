FROM registry.access.redhat.com/ubi10-minimal

RUN microdnf -y --nodocs install \
        git \
        make \
        python3.12 \
    && microdnf clean all
