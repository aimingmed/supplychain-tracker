# Setting Up Tortoise ORM in Kubernetes for all dev, qa, and prod deployments

Eg. To set up Tortoise ORM and initialize the database in the Kubernetes environment for the dev deployment, you need to run the equivalent Aerich commands inside your backend pod.

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

# you must do this tunneling to access the services in the cluster to be accessible from localhost. This is necessary to access the services running in your Minikube cluster from your local machine.

```bash
minikube tunnel --bind-address=0.0.0.0
```

# To add localhost 127.0.0.1 to /etc/hosts file in the server that hosting the kubernetes clusterexit

```bash
127.0.0.1       sctracker-dev.aimingmed.local
127.0.0.1       sctracker-qa.aimingmed.local
127.0.0.1       sctracker.aimingmed.local
```

# for developer use:

```bash
# Diagnosis through logs for each service deployed
kubectl get deployments -n sctracker-dev
kubectl get pods -n sctracker-dev
kubectl logs backendsctracker-7cf84dfd74-lws5k -n sctracker-dev

# check the external network for each service deployed, if any
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
kubectl describe svc ingress-nginx-controller -n ingress-nginx
```
