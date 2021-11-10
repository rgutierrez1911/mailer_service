FROM python:3.8-slim-buster
#!COPYING APP AND REQUIREMENTS
COPY requirements.txt /
COPY . /app

#!DEPENDENCY INSTALATION
RUN pip3 install setuptools
RUN pip3 install -r requirements.txt

#!CHECK OUT APP 
RUN ls -las /app
WORKDIR /app

#!RUNNING APP

CMD  ["python3" , "./app/main.py"]