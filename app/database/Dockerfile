# pull official base image
FROM postgres:17-bookworm

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d

# install python
RUN apt-get update 
RUN apt-get install -y python3 python3-pip python3-venv
RUN python3 -m venv /mnt/venv
RUN apt-get install -y rustc
RUN /mnt/venv/bin/pip3 install sqlalchemy psycopg2-binary openpyxl xlrd pandas==1.5.3 numpy==1.26.4 tortoise-orm==0.20.0 fastapi==0.109.0 pydantic-settings==2.1.0 asyncpg==0.29.0 aerich==0.7.2 "pydantic==2.7.4"
# have to separately downgrade the numpy version
RUN /mnt/venv/bin/pip3 install numpy==1.26.4

