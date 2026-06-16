# D4 — Kubernetes Manifests

K8s manifests for the transaction-api-python service.

## Dry-run Validation

```bash
kubectl apply --dry-run=client -f transaction-api.yaml
```

## Local Cluster (kind/minikube)

```bash
# Build image
docker build -t transaction-api-python:latest ../../services/transaction-api-python

# kind
kind load docker-image transaction-api-python:latest
kubectl apply -f transaction-api.yaml

# Verify
kubectl get pods
kubectl port-forward svc/transaction-api 8080:80
curl http://localhost:8080/health
```

## Teardown

```bash
kubectl delete -f transaction-api.yaml
```
