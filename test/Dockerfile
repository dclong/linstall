FROM dclong/python

COPY dist/xinstall-*.whl /scripts/

RUN pip3 install -U /scripts/xinstall-*.whl \
    && rm /scripts/xinstall-*.whl