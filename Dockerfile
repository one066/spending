FROM python:3.7
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY src/ /app
CMD gunicorn --preload -w 4 -b 0.0.0.0:8008 manage:app
#CMD ["python", "manage.py"]
