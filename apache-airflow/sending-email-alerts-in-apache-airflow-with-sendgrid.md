# Sending Email Alerts in Apache Airflow with Sendgrid

Airflow is the automation tool used to create and manage reproducible data pipelines. There are specific mechanisms to send alerts to users when there is an error when executing these pipelines.

One of the most common ways of sending these alerts is email. Other's include slack, PagerDuty, or Zapier integration. In one of the blogs, I have covered different ways of sending an email with Airflow. This one is specific to SendGrid.

[Sendgrid](https://sendgrid.com/) is a cloud-based service that provides an email SMTP server for you to send emails. The out of the box integration and ease of use is what made Sendgrid the choice of software for most companies. A common alternative for Sendgrid is [AWS SES](https://aws.amazon.com/ses/)

### Setting Up Sendgrid

Before we use SendGrid with Airflow, you to an account with Sendgrid, go ahead and register yourself. You get 100 emails/day on the free plan, which is good enough for this exercise.

Next, you need to authenticate your domain.

![](https://i.imgur.com/t4tNUkM.png)

You will get a set of DNS records to add to the DNS provider on adding your domain name.

### Types of Sendgrid Email Integration

There are two types of email [integration in Sengrid](https://app.sendgrid.com/guide/integrate)

1. Web API
2. SMTP Relay

**Web API** providers SDK in different languages for you to integrate email sending logic to the code.

![](https://i.imgur.com/niZP6eH.png)

**SMTP Relay** is used when you already have an email sending app and want to configure the SMTP server.

Since Airflow already has the email sending logic, it needs the SMTP details to start sending emails.

### Setting up SMTP

Setting up SMTP details is pretty straightforward. You have to give a name for the API key, and your key will be generated.

![](https://i.imgur.com/WZCmZpi.png)

Now it's only a matter of adding it to Airflow.

### Integrate Sendgrid to Airflow

There are two ways you can integrate SendGrid with Airflow.

#### Using Default SMTP

With default SMTP configuration airflow uses the default SMTP email backend `airflow.utils.email.send_email_smtp` to send the email. Set the following airflow configurations and you're good to go

```
AIRFLOW__SMTP__SMTP_HOST=smtp.sendgrid.net
AIRFLOW__SMTP__SMTP_STARTTLS=False
AIRFLOW__SMTP__SMTP_SSL=False
AIRFLOW__SMTP__SMTP_USER=apikey
AIRFLOW__SMTP__SMTP_PASSWORD=<generated-api-key>
AIRFLOW__SMTP__SMTP_PORT=587
AIRFLOW__SMTP__SMTP_MAIL_FROM=<your-from-email>
```

The equivalent `airflow.cfg` looks like this.

```
[smtp]
smtp_host=smtp.sendgrid.net
smtp_starttls=False
smtp_ssl=False
smtp_ssl=apikey
smtp_password=<generated-api-key>
smtp_port=587
smtp_email=<your-from-email>
```

#### Using Airflow SengridProvider

Airflow also has a Sendgrid specific provider, which you can use as follows.

1. Install `pip install apache-airflow-providers-sendgrid`
2. Set the following mandatory param

```
AIRFLOW__EMAIL__EMAIL_BACKEND=airflow.providers.sendgrid.utils.emailer.send_email
AIRFLOW__EMAIL__EMAIL_CONN_ID=sendgrid_default
SENDGRID_MAIL_FROM=hello@thelearning.dev
```

1. From the Airflow UI, create a Connection of type Email and add the Sendgrid SMTP parameters

![](https://i.imgur.com/7qCCjjd.png)

### Testing Email Alert on Failure

That's it. After configuring, you can use any email sending method, but the whole point of this blog is to send alerts on failure. The following DAG has a `PythonOperator`, which will fail no matter what.

```
def my_custom_function():
    raise Exception
​
​
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email':"<to-email>"
}
​
with DAG('example_dag',
         start_date=datetime(2022, 1, 1),
         max_active_runs=1,
         schedule_interval=None,
         default_args=default_args,
         ) as dag:
​
    tn = PythonOperator(
        task_id=f'python_print_date_1',
        python_callable=my_custom_function
    )
```

Add this to your Airflow DAGs, and you will get an email on failure. You can also set `email_on_retry` as `True` to send emails on retry.

Airflow currently does not support `email_on_sucess`. The only way to achieve this is via `EmailOperator` or a custom `PythonOperator.`

--

{% embed url="https://bhavaniravi.substack.com/embed" %} Newsletter embed {% endembed %}
