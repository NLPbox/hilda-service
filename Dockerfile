# We can't distribute the HILDA parser.
#
# You'll need to sign a license agreement with the Prendinger lab and
# get the parser from them.
# Please contact Prof. Helmut Prendinger <helmut@nii.ac.jp>
#
# Afterwards, build the hilda container, as described in
# https://github.com/NLPbox/hilda-docker
FROM hilda

RUN apk add py3-pip && \
    pip3 install hug==2.4.0 pexpect==4.5.0 pytest==3.5.1 sh==1.12.14

WORKDIR /opt/hilda_service
ADD hilda_hug_api.py /opt/hilda_service/

RUN pip3 install pudb ipython # TODO: rm after debug

EXPOSE 8080

ENTRYPOINT ["hug"]
CMD ["-f", "hilda_hug_api.py"]

