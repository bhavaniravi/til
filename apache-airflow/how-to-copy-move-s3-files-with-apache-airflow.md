# How to Copy/Move S3 Files With Apache Airflow

Create an AWS account, and ensure you have the right roles and policies set before proceeding with the following code

```python
from datetime import datetime
from typing import List, Optional, Tuple
from airflow import DAG
from airflow.providers.amazon.aws.operators.s3 import S3FileTransformOperator
import os

# This fixed NEGSIG.SIGEV error
os.environ['no_proxy'] = '*'

DAG_ID = "s3_file_transform"


with DAG(
    dag_id=DAG_ID,
    schedule=None,
    start_date=datetime(2022, 11, 10),
    tags=["example"],
    catchup=False,
) as dag:

    move_files = S3FileTransformOperator(
        task_id="move_files",
        source_s3_key='s3://v-glue-example-bucket/example.txt',
        dest_s3_key="s3://v-glue-example-bucket/processed/{{ ds }}/example.txt",
        transform_script="/bin/cp"
    )
```

1. You can change the `transform_script` form `/bin/cp`  to `/bin/mv` to move files.
2. Note that the `dest_key` has `{{ds}}` in it. This ensures a new blob is created every time the DAG runs.&#x20;
