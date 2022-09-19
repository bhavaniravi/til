---
slug: "deploying-airflow-on-kubernetes"
published_date: 2020-05-02
created_date: 2020-05-03
title: "How to Set up Airflow on Kubernetes?"
template: "post"
draft: false
description: "The blog walks you through the steps on how to deploy Airflow on Kubernetes."
subtitle: "This blog walks you through the steps on how to deploy Airflow on Kubernetes."
tags: ["apache-airflow"]
featuredImgPath: "https://i.imgur.com/duJj4Ei.png"
isexternal: true
---

# Airflow on Kubernetes

This blog walks you through the steps on how to deploy Airflow on Kubernetes. If you to jump on the code directly [here's the GitHub repo](https://github.com/bhavaniravi/airflow-kube-setup). 

## What is Airflow

> Airflow is a platform created by the community to programmatically author, schedule, and monitor workflows.

Airflow lets you define workflow in the form of a directed acyclic graph(DAG) defined in a Python file. The most famous usecase of airflow is data/machine learning engineers constructing data pipelines that performs transformations.

## Airflow with Kubernetes

There are a bunch of advantages of running Airflow over Kubernetes. 

### Scalability
Airflow runs one worker pod per airflow task, enabling Kubernetes to spin up and destroy pods depending on the load.

### Resource Optimization
Kubernetes spins up worker pods only when there is a new job. Whereas the alternatives such as celery always have worker pods running to pick up tasks as they arrive.

## Pre-Requsites

1. Kubectl
2. Docker
3. A Docker image registry to push your Docker images
4. Kubernetes cluster on GCP/AWS.

## Airflow Architechture

Airflow has 3 major components.

1. Webserver - Which serves you the fancy UI with a list of DAGs, logs, and tasks.
2. Scheduler - Which runs on the background and schedules tasks and manages them
3. Workers/Executors - These are the processes that execute the tasks. Worker processes are spun up by Schedulers and tracked on their completion

<figure>


![Airflow Architechture](https://i.imgur.com/fjNn8Ph.png)

</figure>

Apart from these, there are 

1. Dag folders 
2. Log folders
3. Database

There are different kinds of Executors one can use with Airflow. 

1. LocalExecutor - Used mostly for playing around in the local machine.
2. CeleryExecutor - Uses celery workers to run the tasks
3. KubernetesExecutor - Uses Kubernetes pods to run the worker tasks

## Airflow with Kubernetes

On scheduling a task with airflow Kubernetes executor, the scheduler spins up a pod and runs the tasks. On completion of the task, the pod gets killed. It ensures maximum utilization of resources, unlike celery, which at any point must have a minimum number of workers running.

<figure>

![Airflow Kubernetes Architechture](https://i.imgur.com/b58ioMc.png)

</figure>


### Building the Docker Image

The core part of building a docker image is doing a pip install.

```
RUN pip install --upgrade pip

RUN pip install apache-airflow==1.10.10
RUN pip install 'apache-airflow[kubernetes]'
```

We also need a script that would run the `webserver` or `scheduler` based on the Kubernetes pod or container. We have a file called `bootstrap.sh` to do the same.

```
if [ "$1" = "webserver" ]
then
    exec airflow webserver
fi

if [ "$1" = "scheduler" ]
then
    exec airflow scheduler
fi
```

Let's add them to the docker file too.

```
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh
ENTRYPOINT ["/bootstrap.sh"]
```

Let's build and push the image

```
docker build -t <image-repo-url:tag> .
docker push <image-repo-url:tag>
```

### Kubernetes configuration

> This section explains various parts of `build/airflow.yaml.`

1. A Kubernetes deployment running a pod running both webserver and scheduler containers

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
 name: airflow
 namespace: airflow-example
spec:
 replicas: 1
 template:
 metadata:
 labels:
 name: airflow
 spec:
 serviceAccountName: airflow
 containers:
 - name: webserver
 ...
 - name: scheduler
 ...
 volumes:
 ...
 ...
```

3. A service whose external IP is mapped to Airflow's webserver

```yaml
apiVersion: v1
kind: Service
metadata:
 name: Airflow
spec:
 type: LoadBalancer
 ports:
 - port: 8080
 selector:
 name: airflow
```

4. A serviceaccount which with `Role` to spin up and delete new pods. These provide permissions to the Airflow scheduler to spin up the worker pods.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
 name: airflow
 namespace: airflow-example
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
 namespace: airflow-example
 name: airflow
rules:
- apiGroups: [""] # "" indicates the core API group
 resources: ["pods"]
 verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: ["batch", "extensions"]
 resources: ["jobs"]
 verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
--- 
```

5. Two persistent volumes for storing dags and logs

```yaml
kind: PersistentVolume
apiVersion: v1
metadata:
 name: airflow-dags
spec:
 accessModes:
 - ReadOnlyMany
 capacity:
 storage: 2Gi
 hostPath:
 path: /airflow-dags/
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
 name: airflow-dags
spec:
 accessModes:
 - ReadOnlyMany
 resources:
 requests:
 storage: 2Gi
```

7. An airflow config file is created as a kubernetes config map and attached to the pod. Checkout [`build/configmaps.yaml`]()
8. The Postgres configuration is handled via a separate deployment
9. The secrets like Postgres password are created using Kubernetes secrets
10. If you want to additional env variables, use Kubernetes `configmap`.

### Deployment

You can deploy the airflow pods in 2 modes.

1. Use persistent volume to store DAGS
2. Get use git to pull dags from

To set up the pods, we need to run a `deploy.sh` script that does the following
1. Convert the templatized config under `templates` to Kube config files under `build.`
2. Deletes existing pods, deployments. if any in the namespace
3. Create new pods, deployments, and other Kube resources


```
export IMAGE=<IMAGE REPOSITORY URL>
export TAG=<IMAGE_TAG>
cd airflow-kube-setup/scripts/kube
./deploy.sh -d persistent_mode
```

### Testing the Setup

By default, this setup copies all the examples into the dags; we can just run one of them and see if everything is working fine.

1. Get the airflow URL by running `kubectl get services`
2. Log into the Airflow by using `airflow` and `airflow.` You can change this value in `airflow-test-init.sh.`
3. Pick one of the DAG files listed
4. On your terminal run `kubectl get pods --watch` to notice when worker pods are created
5. Click on `TriggerDag` to trigger one of the jobs
6. On the graph view, you can see the tasks running, and on your terminal new pods are created and shut down completing the tasks.
 
### Maintainence and modification

Once it is deployed, you don't have to run this script every time. You can use basic kubectl commands to delete or restart pods.

```
kubectl get pods --watch 
kubectl logs <POD_NAME> <Container_name>
kubectl exec -it $pod_name --container webserver -- /bin/bash
```

## Got a Question?

[Raise them as issues on the git repo](https://github.com/bhavaniravi/airflow-kube-setup/issues)

## References

Apache Airflow. https://airflow.incubator.apache.org/index.html
