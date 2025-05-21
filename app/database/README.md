# database

## build

When building the image, the setup sql script `setup.sql` as well as wrapper scripts are copied to the image.

```bash
cd app
docker-compose build database
```

## run

You can start the database as follows:

```bash
cd app
docker-compose up -d database
```

During startup, the `setup.sql` script is executed to initialize the complete database schema.
The `entrypoint.sh`, `setup.sh` and `Dockerfile` are based on [this tutorial](https://github.com/twright-msft/mssql-node-docker-demo-app).

## to set up the database

To list all databases in the local container, execute the following:


# how to access the database

localhost/127.0.0.1:5432  
username: postgres  
password: postgres  
database: sctracker_dev
