# pull official base image
FROM python:3.10

RUN apt-get update && apt-get -y install cron vim

# set work directory
WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN echo "export PYTHONPATH=$PYTHONPATH:/app" >> /etc/environment
RUN /bin/bash -c "source /etc/environment"

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# copy project
COPY . .
COPY crontab /etc/cron.d/crontab

#CMD [ "python", "/app/src/main.py"]

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

RUN pip list
RUN pip3 list
# run crond as main process of container
CMD ["cron", "-f"]
