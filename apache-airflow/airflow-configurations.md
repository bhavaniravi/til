---
description: Can Airflow Do this?
---

# Airflow Configurations

If you're a Airflow developer the configuration page in the documentation is a gold mine. Most of the times someone asks _Can Airflow do this?_ the answer lies in the configurations page.

Infact I have this page bookmarked in my browser forever. There are so many configurations to tweak different airflow components.&#x20;

**Catchup**&#x20;

Ensure all the dags run only the future runs irrespective of their start date. You can also set this at each dag level.

### Scheduler Performance

There is a whole page in [Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html?highlight=scheduler#fine-tuning-your-scheduler-performance) on which config params to tweak to use the available resources effectively

### Database

**load_default_connections**&#x20;

&#x20;\*\*\*\* This is a new configuration in 2.3.0 but also an odd one out. Setting this to true will create default Airflow connections in the metadata DB

**max_db_retries**

**sql_alchemy_conn**

**sql_alchemy_connect_args**

**sql_alchemy_engine_args**

&#x20;You can pass a variety of parameters to [sqlalchemy engine](https://docs.sqlalchemy.org/en/14/core/engines.html#engine-creation-api). These can be defined as a dictionary

**sql_alchemy_max_overflow**

Manage sqlalchemy **pool** using&#x20;

- **sql_alchemy_pool_enabled,**&#x20;
- **sql_alchemy_pool_pre_ping**
- **sql_alchemy_pool_recycle**&#x20;
- **sql_alchemy_pool_size**

**sql_alchemy_schema**

**sql_engine_collation_for_ids**

**sql_engine_encoding**

---

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
