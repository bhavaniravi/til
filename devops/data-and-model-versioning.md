---
added: Oct 28 2022
draft: false
image: null
layout: ../layouts/BlogPost.astro
slug: data-and-model-versioning
sub_title: What is MLOps? Why we need it? and what tools are available?
tags:
- devops
title: Data & Model Versioning
---

# Data & Model Versioning

### **Why do we need Model Versioning?**

I wrote a model 6 months back. I don't know where it is.

I wrote a model 6 months back. I don't remember what it is. Let me try to find it.

I got 80% accuracy yesterday. I swear.

### **Why do these problems exist?**

Because conventional software engineering process does not work for Machine learning project

Unlike Software Engineering, Machine Learning involves trial and error and experimentation. We need a way to track these experiments.

GitHub is not enough

1\. Data is huge and are often not in CSV itself

2\. Model is huge. We need to store it better

### **Why should we care about it?**

Businesses need an audit. Anything that doesn't have an audit or cannot reproduce results is not production-grade.

### **Toolkit for MLOps**

1\. MLflow

2\. Kubeflow

3\. DVC

### **MLflow**

MLFlow has pretty much has everything that an ML engineer looks for

1\. A dev environment

2\. Place to run and track experiemnets

3\. Build and run pipelines

#### **Disadvantages**

1\. MLflow is a Python library in itself. Hard-core engineers do not want to work with abstractions. It is impossible for them to \`from mlops.sklearn\`

### **Kubeflow**

Kubeflow focuses on the pipeline orchestration of the ML process. Whereas in data versioning, we focus on individual components that define the pipelines

### **DVC - Data version control**

1\. Create a GitHub repo

2\. Create assets directory for \`data\`, \`models\`, \`raw_data\`, \`features.\`

3\. \`dvc init\`

4\. \`dvc add file/directory\`

5\. DVC will create a \`.dvc\` file and a \`.gitignore\` to ignore specific files\\

#### **Experiment tracking and pipelines**

Every time you run the DVC pipeline, the model gets versioned along with the data it is trained on.

#### **Deployment on Kubernetes with DVC**

1\. Add an NFS volume to the pod and mount it to assets

2\. Create a docker image with the DVC repo

3\. On the init script, do a \`dvc pull\`

The DVC remote S3/GCS should be accessible by the Kubernetes cluster
