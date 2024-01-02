---
description: Create multiple airflow tasks based on the output of previous task
---

# Dynamic Task Mapping

Dynamic Task Mapping is the most awaited feature of Apache Airflow. I was waiting for it from 2019 when I started to use Apache Airflow.

The general idea is this let's say you have 3 tasks A -> B -> C. Assuming A reads a bunch of files to be processed by B, and the processing is independent of each other, we want Airflow to spin up tasks B1, B2, B3... depending on output of A

```
              |---> Task B.1 --|
              |---> Task B.2 --|
 Task A ------|---> Task B.3 --|-----> Task C
              |       ....     |
              |---> Task B.N --|
```

From the looks of it, it might look like a simple feature but since the DAGs and tasks are generated before the tasks are executed achieving this during Dag runtime was a problem.

**But, not after Airflow introduced Dynamic Task Mapping in 2.3**

### Dynamic Task Mapping

***

```python
from airflow import DAG
from airflow.decorators import task
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from datetime import datetime

@task
def get_s3_files(current_prefix):
    s3_hook = S3Hook(aws_conn_id='s3')
    current_files = s3_hook.list_keys(bucket_name='my-bucket', prefix=current_prefix + "/", start_after_key=current_prefix + "/")
    return [[file] for file in current_files]


with DAG(dag_id='mapping_elt',
        start_date=datetime(2022, 4, 2),
        catchup=False,
        template_searchpath='/usr/local/airflow/include',
        schedule_interval='@daily') as dag:

    move_s3 = S3CopyObjectOperator.partial(
        task_id='move_file',
        aws_conn_id='s3',
        source_bucket_name='my-new-bucket',
        source_bucket_key="{{ ds_nodash }}"+"/",
        dest_bucket_name='my-bucket',
        dest_bucket_key="{{ ds_nodash }}"+"/"
    ).expand(s3_keys=get_s3_files(current_prefix="{{ ds_nodash }}"))

```

**More documentation and example here:**

* [Official Dynamic Task Mapping documentation](https://airflow.apache.org/docs/apache-airflow/2.3.0/concepts/dynamic-task-mapping.html)
* [Tutorial from Astronomer](https://www.astronomer.io/guides/dynamic-tasks)

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
