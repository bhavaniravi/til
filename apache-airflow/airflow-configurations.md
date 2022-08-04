---
description: Can Airflow Do this?
---

# Airflow Configurations

## max\_active\_runs and max\_queued\_dag\_runs

Description: Differentiating the behavior of max\_active runs in 1.x and 2.x and 2.2.x Priority: 1 Specialization: Airflow Status: ReadyToRecord

1. Introducing `max_active_runs` in config level and dag level in 1.x
2. Change the params to 1, 2, 3 etc.,

```jsx
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
import time

def my_custom_function(ti):
		time.sleep(10)
    print ("hello")

default_args = {
    "start_date": days_ago(1),
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

with DAG('example_dag_copy',
         max_active_runs=1,
         schedule_interval=None,  
         default_args=default_args,
         catchup=False
         ) as dag:

        tn = PythonOperator(
            task_id=f'python_print_date',
            python_callable=my_custom_function,  # make sure you don't include the () of the function
            provide_context=True,
        )
```

1. Introduction of queued state in 2.x
2. `max_active_runs` and `max_queued_dag_runs` in 2.x
3. **`max_queued_runs_per_dag` is removed in latest 2.2.0 so it's better not to use it**
4. Now `max_queued_active_runs` is handled by `max_active_run`
