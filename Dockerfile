FROM python:3

ENV HOME /root
WORKDIR /root

#RUN pip3 install

COPY . .


EXPOSE 8000

CMD [ "python", "./main.py" ]