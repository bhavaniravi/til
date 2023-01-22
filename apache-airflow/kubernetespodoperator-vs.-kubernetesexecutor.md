# KubernetesPodOperator vs. KubernetesExecutor

### KubernetesExecutor

KubernetesExecutor is where Airflow spins up a new pod to run an Airflow task. Unlike Celery executor the advantage is you don't have a bunch of workers always running. KubernetesExecutor is on-demand thereby reducing cost.\

One dowside of kubernetes executor can be the time it takes to spin up the pod but compared to the advantages it can be close to null

### KubernetesPodOperator

When using `KubernetesPodOperator`, all the business logic and it's associated code resides in a docker image. During execution, airflow spins up a worker pod, which pulls the mentioned docker image and executes the respective command.

```
KubernetesPodOperator(
        task_id='classify_tweets',
        name='classify_tweets',
        cmds=['python', 'app/classify.py'],
        namespace='airflow',
        image='gcr.io/tweet_classifier/dev:0.0.1')
```

#### Pros

1. Works well across cross-functional teams
2. Single airflow instance can be shared across teams without hassle
3. Supports different languages and frameworks
4. Decouples DAG and the business logic

---

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
