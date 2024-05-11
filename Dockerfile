FROM python:3.9
WORKDIR /app

COPY app/requirements.txt /app/
RUN apt-get update && apt install -y libpq-dev && apt-get install -y gcc
RUN pip3 install -r /app/requirements.txt
#ENV LISTEN_PORT 5000
EXPOSE 5000
COPY ./app /app
#RUN chmod +x app/StartApplication.sh
CMD ["python", "app.py"]
