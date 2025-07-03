# How to work with this app repository

Build the images:

```bash
docker compose up --build -d
```

If this is first time setting up database schema, run the following command to create the database schema:

```bash
docker compose exec backend pipenv run aerich init -t db.TORTOISE_ORM;
docker compose exec backend pipenv run aerich init-db
```

If already previously set up the database schema, apply the migrations:

```bash
# run this if you have made changes to the models
docker compose exec backend pipenv run aerich migrate --name "DepMapCellLineProfile-lineage_2-increaseLengthTo100"
# else just run this, it will set up the database schema
docker compose exec backend pipenv run aerich upgrade

# if you want to downgrade to previous version, you can use:
# $ docker compose exec backend pipenv run aerich downgrade --name <version_name>

# prefer just to apply the latest changes to the database, without the migrations?
# $ docker compose exec backend pipenv run python backend/db.py
```

# Run the tests for backend:

```bash
docker compose exec backend pipenv run python -m pytest --disable-warnings --cov="."
```

Lint:

<!-- ```bash
docker compose exec backend pipenv run flake8 tests
``` -->

Run Black and isort with check options:

```bash
docker compose exec backend pipenv run black . --check
docker compose exec backend pipenv run isort . --check-only
```

Make code changes with Black and isort:

```bash
docker compose exec backend pipenv run black .
docker compose exec backend pipenv run isort .
```

# Postgres

Want to access the database via psql?

```bash
docker compose exec -it database psql -U postgres
```

Then, you can connect to the database and run SQL queries. For example:

```sql
# \c sctracker_dev
# \dt
```

DROP TABLE IF EXISTS requestdetails;
TRUNCATE TABLE aerich;