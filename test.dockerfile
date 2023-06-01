FROM python:3.10

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

CMD python -m unittest discover tests/ -p '*.py'

