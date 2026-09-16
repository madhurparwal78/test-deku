FROM deku-verifier-base

COPY workflows.yaml /tests/workflows.yaml
COPY rubric.json /tests/rubric.json
COPY conftest.py /tests/conftest.py
COPY test_output.py /tests/test_output.py
COPY test.sh /tests/test.sh

RUN chmod +x /tests/test.sh
