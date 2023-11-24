---
runme:
  id: 01HFX9MNKSMC7S3VM1Z3SCQTBQ
  version: v2.0
---

To create Kubernete PostgreSQL database

```sh {"id":"01HFYF06A97WZF4A2S3RMC1ENN"}
kubectl create namespace db-postegs
```

```sh {"id":"01HFYF06A97WZF4A2S3T1JNM10"}
kubectl apply -f db-configmap.yaml
```

```sh {"id":"01HFYF06A97WZF4A2S3XY6XQ5W"}
kubectl apply -f db-persistent-volume.yaml
```

```sh {"id":"01HFYF06A97WZF4A2S3VDHMW44"}
kubectl apply -f db-persistent-volume-claim.yaml
```

```sh {"id":"01HFYF06A97WZF4A2S4193EZSH"}
kubectl apply -f db-service.yaml
```

```sh {"id":"01HFYF06A97WZF4A2S4246C0HV"}
kubectl apply -f db-deployment.yaml
```

```sh {"id":"01HFYH9Y9XRR5PGXSR96E9VQ7M"}
kubectl get pvc -n db-postegs
```

```sh {"id":"01HFZ2GWPGSPS930CKER9FV43E"}
kubectl get all -n db-postegs
```

```sh {"id":"01HFYH9Y9XRR5PGXSR991JWQK0"}
kubectl describe pod/postgresdb-7999bf7b8-f9qhx -n db-postegs
```

Destroy All

```sh {"id":"01HFYF06A97WZF4A2S42E9HP7E"}


kubectl delete all --all -n db-postegs

kubectl delete svc --all -n db-postegs

kubectl delete configmap --all -n db-postegs

kubectl delete secret --all -n db-postegs

kubectl delete pvc --all -n db-postegs

kubectl delete pv --all -n db-postegs

kubectl delete namespace db-postegs
```

To connect in Network TPC use "postgresql://postgres:5432/sonar_db"