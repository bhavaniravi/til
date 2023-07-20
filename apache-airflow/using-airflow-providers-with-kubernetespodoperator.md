# Using Airflow Providers With KubernetesPodOperator

When you're constrained to use KubernetesPodOperator you will be at a disadvantage of using Airflow providers. There is something you can do about it. Using Airflow provider like any other library.

1. Install airflow and associated providers you need in the Docker image, KubernetesPodOperator will be using.
2. Create a python script that will be consumed by KubernetesPodOperator
3. Inside the script, import the provider operator and call its execute method

```
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator

create_object = S3CreateObjectOperator(
    task_id="s3_create_object",
    s3_bucket=BUCKET_NAME,
    s3_key=KEY,
    data=DATA,
    replace=True,
)

create_object.execute(dict())
```



{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
