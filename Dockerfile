FROM python:3.8.10
ENV PYTHONUNBUFFERED 1
WORKDIR /chellaboina
ADD . /chellaboina/
EXPOSE 8080
COPY requirements.txt /chellaboina
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "manage.py","runserver","0.0.0.0:8080" ]