---
title: How to Send Email Alerts from Airflow?
sub_title: Email task status or Send reports from Airflow
slug: sending-emails-from-airflow
tags:
  - apache-airflow
featuredImgPath: https://i.imgur.com/BBjdWBE.png
isexternal: true
published_date: "2021-01-10"
created_date: "2021-01-10"
draft: false
description: >-
  Airflow allows multiple ways to keep the users informed about the status of a
  task. There is no one size fit all solution when it comes to sending emails
  from airflow. We will deep dive into all the m
---

# How to Send Email Alerts from Airflow?

Airflow is an open-source workflow management software by apache if you are new to Airflow [check out the introduction blog](apache-airflow-introduction.md).

Now that you understand what Airflow is, let's discuss how you can send emails to update your team about the status of a task or send reports using airflow.

## Sending Email from Airflow

There is no one size fit all solution when it comes to sending emails from airflow. We will deep dive into all the methods available and the pros and cons of each in the following sections.

If you're not sure what an SMTP server is or how to configure one. Checkout the SendGrid blog&#x20;

{% content-ref url="sending-email-alerts-in-apache-airflow-with-sendgrid.md" %}
[sending-email-alerts-in-apache-airflow-with-sendgrid.md](sending-email-alerts-in-apache-airflow-with-sendgrid.md)
{% endcontent-ref %}

All the methods below need an SMTP server, and the same to be configured in the `airflow.cfg` file.

```
[smtp]
smtp_host = localhost
smtp_starttls = True
smtp_ssl = False
smtp_user = airflow
smtp_password = airflow
smtp_port = 25
smtp_mail_from = omid@example.com
```

## Email Operator

Airflow comes with an operator to send emails. Import the operator, configure the subject and the email body, you have an email ready to be sent.

```
from airflow.operators.email_operator import EmailOperator

email = EmailOperator(
        task_id='send_email',
        to='to@gmail.com',
        subject='Airflow Alert',
        html_content=""" <h3>Email Test</h3> """,
        dag=dag
)
```

## Operator Options

Every operator in airflow comes with an option to send an email on failure/success.

1. `email_on_failure` - To send an email of failure
2. `email_on_retry` - Send an email if the task failed and before retry
3. `email` - The `to` email address(es) used in email alert

```
python_task = PythonOperator(
                task_id='my_python_task',
                python_callable=print_hello,
                email_on_failure=True
                dag=dag
            )
```

Email operators and email options are the most simple and easy way to send emails from airflow. The only drawback is these options are limited in customization.

One common use case for sending emails is to send reports of tasks executed in the pipeline. For such cases, you might want to construct an email body based on the success or failure of tasks.

## Using Callback

The above use case can be achieved using a callback mechanism. Let's start by writing a generic function to send an email. Different callback mechanisms can repurpose this function.

```
def send_email(**context):

    task = context['ti'].task
    for parent_task in task.upstream_list:
        ti = TaskInstance(parent_task, args.execution_date)
        if ti.current_state() == "FAILURE":
            status = "Failed"
            break
        else:
            status = "Successful"


    subject = "Order {status}""
    body = f"""
        Hi {user}, <br>
        # Type your message here

        <br> Thank You. <br>
    """

    send_email(dag.default_args["email"], subject, body)
```

### Task Level callback

Each task in Airflow comes with callbacks for `success` or `failure` of tasks. We can define this callback function to send an email per task.

This works well when your pipeline is small or when you want the status of a particular task.

But oftentimes, we want to email about the status of the whole pipeline.

```
from airflow.operators.python_operator import PythonOperator

python_task = PythonOperator(
        task_id='my_python_task',
        python_callable=failure_func,
        on_failure_callback=send_email,
        provide_context=True
        dag=dag
    )
```

### DAG level Callback

Just like tasks, DAGs also have callbacks. This method will be called after the completion of all tasks on the DAG.

```
dag = DAG(
    dag_id='example_dag',
    start_date=datetime(2020, 1, 1),
    on_failure_callback=send_email
)
```

While callbacks completely fit our purpose, there is still one problem. With callbacks, we lose the advantage we have by treating them as an independent task.

1. Whether the email sending was a success or failure?
2. how long did it take to send the email?
3. What are the logs?
4. When did it run?
5. How many emails sent?

## PythonOperator

To achieve the combined benefits of customization and added advantage of airflow task, we can couple the above send_email function to an airflow `PythonOperator.`

```
email_task = PythonOperator(
      task_id="email_status",
      python_callable=email_notification,
      provide_context=True,
      dag=dag,
      trigger_rule=TriggerRule.ALL_DONE,
)
```

---

Keeping your stakeholders notified would be an important part of any workflow. Emails are the easiest way to achieve that.

### Next Up...

{% content-ref url="sending-email-alerts-in-apache-airflow-with-sendgrid.md" %}
[sending-email-alerts-in-apache-airflow-with-sendgrid.md](sending-email-alerts-in-apache-airflow-with-sendgrid.md)
{% endcontent-ref %}

---

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
