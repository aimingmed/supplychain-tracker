# pull official base image
FROM python:3.11.11-slim-bookworm

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install build-essential netcat-traditional gcc postgresql \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip setuptools wheel -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple 
COPY ./Pipfile .
RUN pipenv install --deploy --dev

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]