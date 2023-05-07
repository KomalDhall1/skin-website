FROM python:alpine3.8

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . . 
EXPOSE 5000
CMD ["python","app.py",]
