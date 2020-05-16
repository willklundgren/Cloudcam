FROM resin/raspberry-pi-python:3

RUN pip install picamera

COPY main.py /main.py

CMD [ "python3", "-u", "./main.py" ]