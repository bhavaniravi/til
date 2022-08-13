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

**load\_default\_connections**&#x20;

&#x20;**** This is a new configuration in 2.3.0 but also an odd one out. Setting this to true will create default Airflow connections in the metadata DB

**max\_db\_retries**

**sql\_alchemy\_conn**

**sql\_alchemy\_connect\_args**

**sql\_alchemy\_engine\_args**

&#x20;You can pass a variety of parameters to [sqlalchemy engine](https://docs.sqlalchemy.org/en/14/core/engines.html#engine-creation-api). These can be defined as a dictionary

**sql\_alchemy\_max\_overflow**

Manage sqlalchemy **pool** using&#x20;

* **sql\_alchemy\_pool\_enabled,**&#x20;
* **sql\_alchemy\_pool\_pre\_ping**
* **sql\_alchemy\_pool\_recycle**&#x20;
* **sql\_alchemy\_pool\_size**

**sql\_alchemy\_schema**

**sql\_engine\_collation\_for\_ids**

**sql\_engine\_encoding**



