---
slug: kubernetes-101-deploy-apps-in-kubernetes
title: Deploying Flask Applications in Kubernetes (Digitalocean)
sub_title: Basics of kubernetes and deploying apps in K8 environment
tags:
  - devops
featuredImgPath: https://i.imgur.com/uTbgOJD.png
isexternal: true
published_date: 2022-03-06T00:00:00.000Z
created_date: 2022-03-06T00:00:00.000Z
draft: false
description: >-
  The word Kubernetes and the keywords around it are scary for people. In this
  blog, we will demistify what those words mean and how to deploy a web
  application in kuberenetes environment
---

# Deploying Flask Applications in Kubernetes (Digitalocean)

## What is Kubernetes?

Kubernetes, aka K8s, are container orchestration tools. We saw what containers are and how they work in the previous blogs. Kubernetes lets you run and manage these containers in a controlled manager.

## Why use K8s?

The advantage of using a container is that it's OS independent, lightweight, shippable. Another significant advantage is that you can scale the containers up and down without much overhead. Container orchestration tools like Kubernetes let you do this seamlessly.

Yes, Kubernetes is too much to wrap your head around. So let's take it to step by step.



## Kubernetes Resources

Let's repeat this Kubernetes is a container orchestration tool. It will create, run and destroy containers. It is not an OS. It is not a physical/virtual machine. For Kubernetes to run the containers, it needs an external physical or virtual machine. These machines are called **Nodes**

In Kubernetes, we have more than one Node working together and hence bringing us to the concept of **Cluster**

Inside every Node, we will have the capabilities to run the containers in a small unit called **Pod**. The Pod specifies what container to run.

When you want to run the same container(Pod) many times, you can define a **Deployment**

Once the application is running inside the Pod, you will expose it to the outside world via the **Service**

With that, we have got a high-level understanding of the most used Kubernetes keywords

* Pod
* Deployment
* Service
* Node
* Cluster
* Namespace

We will see more resources as we go along this journey. For now, let's see how to set up a cluster and expose it using the resources mentioned earlier on Digitalocean.

## Why Digitalocean?

Because I have some free credits, you can spin up one at just 10$/month.

[With my referral link, get 100$ worth credits instantly](https://m.do.co/c/41c2c624a048)

## Sample Application

For simplicity's sake, I will use a simple "Todo" flask application as a sample. The step-by-step development of this app has been shared in [Build your first flask app tutorial](https://medium.com/bhavaniravi/build-your-1st-python-web-app-with-flask-b039d11f101c)

Remember, you can host any application in any language on a Kubernetes environment.

## Setting up a Kubernetes Cluster

You can spin up a Kubernetes cluster without hassle in any managed services such as AWS, GCP, or Digitalocean. Note that these managed services come out of the box. You can also install Kubernetes on a bare-metal machine like you do any other software. But that is a problem for another time.

For now, check out how to create a K8 cluster on Digitalocean from [here](https://docs.digitalocean.com/products/kubernetes/quickstart/#create-clusters)

## DigitalOcean CLI

I hope you have your Digitalocean account set up?

> You might need to pay a 5$ fee initially and set up your card. Remove it later. You won't be charged any.

Digitalocean CLI tool is terrific for creating Kubernetes resources. I use it the most for manipulating Kubernetes resources and pushing docker images. To do that, you need to authenticate your Command line with an access token.

1. Install `doctl`, a cmd line tool to Digitalocean
2. In Digitalocean site, [under API, create a personal access token](https://cloud.digitalocean.com/account/api/tokens)

```
export DO_TOKEN=<Token-here>
doctl auth init -t $DO_TOKEN
```

## How to deploy an application in the Kubernetes cluster

Now for the fun part. What do you need to deploy?

* Dockerized sample application
* Kubectl access
* Kubernetes spec

Let's do this one by done.

### Dockerize Application

Download the [sample application from Github](https://github.com/bhavaniravi/flask-tutorial) and see if you can run it.

```
# -t stands for tag
docker build -t flask-tutorial:0.0.1

# -it stands for interactive terminal
docker run -it flask-tutorial
```

Does the application run in your local machine? Good, it means it will also run in Kubernetes.

### Docker Registry

Now the application runs on your local machine. You need it somewhere on the cloud for the Kubernetes cluster to access it. Like how "Google Drive" stores your files, the "Docker Registry" store docker images. One can use DockerHub, which is a registry provided by Docker. There are similar options to GCR(Google) ECR(AWS). We are going to use Digitalocean's container registry.

To create a registry in Digitalocean.

1. Go to [https://cloud.digitalocean.com/registry](https://cloud.digitalocean.com/registry)
2. Give a registry name
3. Select a plan and click "Create registry."

The docker images can be referenced by registry, image, and tag. Currently, we have created the `flask-tutorial:0.0.1` tag. Let's map it to a registry tag. Let's re-tag this image in the `<registry-name>/<image-name>/<image-tag>`

```
docker tag flask-tutorial:0.0.1 registry.digitalocean.com/do-registry/flask-tutorial:1.0.0
doctl registry login
docker push registry.digitalocean.com/do-registry/flask-tutorial:1.0.0
```

### Create Kubernetes Cluster

Follow [Digitalocean Cluster creation tutorial and create a Kubernetes cluster](https://docs.digitalocean.com/products/kubernetes/how-to/create-clusters/)

### Kubectl Access

To create kubectl resources like pods, deployments, etc., you need kubectl and cluster config. A DevOps engineer will work with multiple Kubernetes Cluster. The cluster config has information about the Cluster and lets you switch between them.

```
doctl Kubernetes cluster kubeconfig save terraform-do-cluster
```

To list all the configured clusters.

```
kubectl config get-clusters
```

Choose the Cluster you want to work with

```
kubectl config use-context <cluster-name>
```

### Deploying Flask App

1. Create a new namespace. Every kube resource related to this app will be in this namespace

```
kubectl get namespaces
kubectl create namespace todoapp
kubectl config set-context --current --namespace=todoapp
```

1. Create Pod, deployment spec. Create a file `deployment.yaml`

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todoapp
  labels:
    app: todoapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todoapp
  # pod spec begins here
  template:
    metadata:
      labels:
        app: todoapp
    spec:
      containers:
        - name: todoapp
          image: registry.digitalocean.com/bee-do-registry/flask-app:1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8888
```

1. Create a service spec in file `service.yaml` to expose your application to the outside world. I have created a service of type `LoadBalancer` for ease of usage. But it is always a good idea to have an ingress installed at the Cluster and route your request to a `ClusterIP` type service.

```
apiVersion: v1
kind: Service
metadata:
  name: todoapp
spec:
  ports:
  - port: 8888
    protocol: TCP
    targetPort: 8888
  selector:
    app: todoapp
  type: LoadBalancer
```

## Running Application

You can check the running pods and services using the following command

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get service # wait until external IP is set
```

Open the browser and hit `http://<external-ip>:8000/`, you should see the flask homepage.

To check the logs use

```
kubectl get logs -f <pod-name>
```

We have just nicked the surface of Kubernetes. You can create a custom resource with other resources, and there is this whole unexplored territory of how Kubernetes works internally. We will explore all of these in the upcoming articles.



{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
