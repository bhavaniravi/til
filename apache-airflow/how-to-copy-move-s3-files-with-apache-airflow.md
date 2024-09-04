---
added: Nov 28 2022
draft: false
image: null
unusedLayout: ../layouts/BlogPost.astro
slug: how-to-copy-move-s3-files-with-apache-airflow
sub_title: With Apache-Airflow's AWS providers S3 operations are a cake-walk.
tags:
- apache-airflow
title: How to Copy/Move S3 Files With Apache Airflow
---

# How to Copy/Move S3 Files With Apache Airflow

1. Create an AWS account, and ensure you have the [right roles and policies](../devops/aws/iam-users-roles-and-policies.md) set before proceeding with the following code
2. Create a working instance of Apache Airflow in local or on your preferred cloud provider
3. Create an Airflow connection with `AWS_SECRET, AWS_ACCESS and role_arn`
4. The connection extras will look something like this. Replace `<your-role-arn>` with the AWS role that you created.\\

   `{"region_name": "us-west-2", "role_arn": "<your-role-arn>", "assume_role_method": "assume_role"}`

5. Add the following DAG to your dags folder
6. Run the code

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

1. You can change the `transform_script` form `/bin/cp` to `/bin/mv` to move files.
2. Note that the `dest_key` has `{{ds}}` in it. This ensures a new blob is created every time the DAG runs.
3. You can also pass a python script as a string to `transform_script`
