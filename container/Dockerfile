FROM python:3.6-slim-jessie
MAINTAINER wangkun_lc@inspur.com

RUN mkdir /watcher /exec /workspace

COPY watcher.py /watcher/watcher.py
COPY requirements.txt /watcher

WORKDIR /watcher
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

VOLUME [ "/exec", "/workspace" ]

CMD [ "python", "watcher.py"]
