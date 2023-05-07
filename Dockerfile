FROM python:alpine3.8

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . . 
EXPOSE 5000
CMD ["python","app.py",]
