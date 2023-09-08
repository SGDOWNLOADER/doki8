FROM miraclemie/alpine:3.18
RUN apk add --no-cache libffi-dev \
    && apk add --no-cache $(echo $(wget --no-check-certificate -qO- https://raw.githubusercontent.com/SGDOWNLOADER/doki8/master/package_list.txt)) \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && if [ "$(uname -m)" = "x86_64" ]; then ARCH=amd64; elif [ "$(uname -m)" = "aarch64" ]; then ARCH=arm64; fi \
    && curl https://dl.min.io/client/mc/release/linux-${ARCH}/mc --create-dirs -o /usr/bin/mc \
    && chmod +x /usr/bin/mc \
    && mkdir -p /root/.pip \
    && echo $'[global] \n\
    timeout = 600 \n\
    index-url = https://pypi.tuna.tsinghua.edu.cn/simple \n\
    trusted-host = pypi.tuna.tsinghua.edu.cn \n'\
    > /root/.pip/pip.conf \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r https://raw.githubusercontent.com/SGDOWNLOADER/doki8/master/requirements.txt \
    && apk del libffi-dev \
    && rm -rf /tmp/* /root/.cache /var/cache/apk/* \
    && pip cache purge
ENV LANG="C.UTF-8" \
    PS1="\u@\h:\w \$ " \
    REPO_URL="https://github.com/SGDOWNLOADER/doki8.git" \
    DOKI8_VERSION=master \
    PUID=0 \
    PGID=0 \
    UMASK=000 \
    WORKDIR="/doki8"
WORKDIR ${WORKDIR}
RUN echo 'fs.inotify.max_user_watches=524288' >> /etc/sysctl.conf \
    && echo 'fs.inotify.max_user_instances=524288' >> /etc/sysctl.conf \
    && git config --global pull.ff only \
    && git clone -b ${DOKI8_VERSION} ${REPO_URL} ${WORKDIR} --depth=1 --recurse-submodule \
    && git config --global --add safe.directory ${WORKDIR}
CMD ["python", "/doki8/run.py"]
