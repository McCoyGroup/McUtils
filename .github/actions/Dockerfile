# GitHub Actions container to support doing CI
FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

LABEL "name"="McCoyGroup/McUtilsCI"
LABEL "maintainer"="Mark Boyer <maboyer@tamu.edu>"
LABEL "version"="0.0.1"

LABEL "com.github.actions.name"="McUtils Continuous Integration"
LABEL "com.github.actions.description"="Runs CI for the McUtils package"
LABEL "com.github.actions.icon"="git"
LABEL "com.github.actions.color"="orange"

RUN \
    pip install --upgrade pip && \
    pip install git+https://github.com/McCoyGroup/McUtils.git

RUN \
    cd /home && \
    git config --system --add safe.directory /github/workspace && \
    git clone https://github.com/McCoyGroup/McUtils.git

ENTRYPOINT ["/bin/bash", "/home/McUtils/ci/run_ci.sh"]