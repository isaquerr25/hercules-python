---
runme:
  id: 01HFX9FAFX03S2YX3RKGRRXAAY
  version: v2.0
---

info: https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html

Create the ecr in the AWS "not in code"

need get configuration ecr

need run this to create configuration aws ecr

```sh {"id":"01HFZ73GP54PHSX9HP2NAWAKP5"}
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin xxxxxxxx.dkr.ecr.us-east-1.amazonaws.com
```

For see if this made login

```sh {"id":"01HFZ73GP54PHSX9HP2RPXMBXC"}
cat ~/.docker/config.json
```

To Create The Image

```sh {"id":"01HFZ73GP54PHSX9HP2VTSSCFX"}
docker build -t hercules .
```

```sh
aws ecr get-login-password --region us-east-1 
```

To Rename

```sh {"id":"01HFZ73GP54PHSX9HP2YZ1DF3E"}
docker tag hercules:latest xxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/hercules:latest
```

To made push for private repositorie

```sh {"id":"01HFZ73GP54PHSX9HP321KRNZH"}
docker push xxxxxxx.dkr.ecr.us-east-1.amazonaws.com/hercules:latest
```

To connect kubernetes to ecr

1. First need get the temporary key AWS

```sh {"id":"01HFZ73GP690X0KR551V3N6BXH"}
aws ecr get-login-password --region us-east-1
```

2. Get the key from the last operation and change the value (--docker-password=)

```sh {"id":"01HFZ73GP690X0KR551VH91QDV"}
kubectl create secret docker-registry regcred --docker-server=https://xxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com --docker-username=AWS --docker-password=xxxxx --docker-email=harccccci.kaccccccccmmana@gmail.com

```

Add in the deployments. The "imagePullSecrets" the value secrets pod "regcred" for user the keys aws

To delete the key use:

```sh {"id":"01HFZ73GP690X0KR551WY9JHJ6"}
kubectl delete secret regcred
```

learn : https://www.youtube.com/watch?v=oG1wYgKg4NA

learn : https://www.youtube.com/watch?v=asIS4KIs40M

ref: https://docs.microfocus.com/doc/Data_Center_Automation/2023.05/Createimagepullreg
