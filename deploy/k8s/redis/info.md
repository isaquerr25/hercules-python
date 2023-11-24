---
runme:
  id: 01HFYGPFH7PPGSWX371S4Y07RJ
  version: v2.0
---

need create name space

```sh
kubectl create namespace redis-server
```

```sh
kubectl apply -f redis-pv.yaml

kubectl apply -f redis-pvc.yaml

kubectl apply -f service-service.yaml

kubectl apply -f redis-deployment.yaml

```

```sh
kubectl get all -n redis-server
```

```sh
kubectl get pv  -n  redis-server
```

```sh
kubectl get pvc  -n  redis-server
```

```sh
kubectl describe pod/redis-server-7b4ff9df78-tcvsb -n redis-server
```

artigo: https://rpi4cluster.com/k3s/k3s-redis/#

```sh
kubectl delete namespace redis-server

kubectl delete all --all -n redis-server

kubectl delete pvc --all -n redis-server

kubectl delete svc --all -n redis-server
```
