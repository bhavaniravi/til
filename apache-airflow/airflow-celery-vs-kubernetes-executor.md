# Airflow Celery vs Kubernetes Executor

### CeleryExecutor

Celery is used for running distributed asynchronous python tasks.

Hence, CeleryExecutor has been a part of Airflow for a long time, even before Kubernetes.

CeleryExecutors has a fixed number of workers running to pick-up the tasks as they get scheduled.

**Pros**

1. It provides scalability.
2. Celery manages the workers. In case of a failure, Celery spins up a new one.

**Cons**

1. Celery needs RabbitMQ/Redis to for queuing the task, which is reinventing the wheel of what Airflow already supports.
2. The above dependency also makes the setup complex.

### KubernetesExecutor

KubernetesExecutor is where Airflow spins up a new pod to run an Airflow task. Unlike Celery executor the advantage is you don't have a bunch of workers always running. KubernetesExecutor is on-demand thereby reducing cost.\


One dowside of kubernetes executor can be the time it takes to spin up the pod but compared to the advantages it can be close to null


--- 

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}