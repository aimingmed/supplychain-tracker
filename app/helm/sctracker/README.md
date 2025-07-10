# Setting Up Tortoise ORM in Kubernetes

To set up Tortoise ORM and initialize the database in the Kubernetes environment, you need to run the equivalent Aerich commands inside your backend pod.

```bash
# Get the backend pod name
kubectl get pods -n sctracker-dev

# Open a shell in the backend pod
kubectl exec -it <backend-pod-name> -n sctracker-dev -- /bin/sh

# Run the Aerich initialization commands
pipenv run aerich init -t db.TORTOISE_ORM
pipenv run aerich init-db

# If you have already initialized before and just want to apply migrations
pipenv run aerich migrate --name "your_migration_name"
pipenv run aerich upgrade
```
