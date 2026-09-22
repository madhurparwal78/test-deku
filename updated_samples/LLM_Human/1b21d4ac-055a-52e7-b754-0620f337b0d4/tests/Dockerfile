# Self-contained verifier. No private base image: this builds from upstream
# python plus the capability modules that ship beside it, so anyone who can
# reach Docker Hub can grade this bundle.
#
# Versions match environment/Dockerfile exactly. Under
# `environment_mode = "shared"` the verifier and the app share a runtime, and a
# pytest that differed between them would grade on a stack the agent never had.
FROM python:3.12-slim

# curl is the health gate in test.sh; nothing else here needs a shell tool.
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      pytest==8.4.1 \
      pytest-json-ctrf==0.3.5 \
      httpx==0.28.1 \
      psycopg[binary]==3.2.3 \
      pyyaml==6.0.2

# The baseline snapshot in test.sh imports capabilities from a bare `python3 -`,
# which inherits no rootdir, so the path is set rather than assumed.
ENV PYTHONPATH=/tests

COPY appclient.py capabilities.py score.py deku_state.py pytest.ini _shapes.py \
     workflows.yaml rubric.json conftest.py test_roster.py test.sh /tests/

WORKDIR /tests
