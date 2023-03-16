---
description: Not a big fan of minikube? Kind should be your thing.
---

# Local K8 Cluster With Kind

Setting up a full-blown Kubernetes cluster on GKE/EKS (GCP/AWS) for side projects isn't a great solution. Sometimes I go for weeks, sometimes months, without working on my side projects. In that case, spinning up and destroying cloud solutions sounds like an overkill

Kind K8 clusters are great because it's simple, easy to use, and just work.&#x20;

### What about Minikube?&#x20;

I have tried minikube but had trouble setting up VMs and left it at that. Now minikube supports Docker, but that doesn't nudge me to give it another shot.

### Installation

I'm on a mac, and there are ways to install it in Windows and Linux.

```
brew install kind
```

### Creating a Cluster

After this, I don't follow the quickstart because I need a cluster with 3 nodes one for kubesystem and 2 for my applications. Write the following into a yaml file `kind-cluster.yaml` and have it handy

```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Kind internally uses Docker containers as your nodes, so you need to have docker up and running.

```
kind create a cluster --config kind-cluster.yml
```

### Get Clusters

To check if clusters are created and their status

```
kind get clusters
```

### Setting Cluster Context to Kubectl

To use this cluster with kubectl, you need to configure the cluster context

```
kubectl cluster-info --context kind-kind
```

Now you can continue on to using the kind cluster as you would use EKS/GKE

### Gotchas

* Running a lot of nodes might slow down your laptop
* Pausing Docker is a new feature. I tried it, only for my system to crash completely. I suggest quitting Docker to release resources and restarting when you need it.
