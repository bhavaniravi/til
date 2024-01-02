---
title: DLTHub - The New ELT tool in the market
sub_title: Should you use DLTHub for your ELT usecase?
slug: DLTHub-new-tool
tags:
  - data-engineering
featuredImgPath:
isexternal: true
published_date: "2023-07-07"
created_date: "2023-07-07"
draft: false
description: >-
    Businesses produce and accumulate data. Before making sense of this data, we must bring them to a centralized place—a data lake. Whenever you can think of data, movement tools like Fivetran comes into the picture.
    DLTHub is an ELT(Extract, Load, Transform) accumulating its market of Fivetran by using open source to its advantage.
---

# 🔗 DLTHub - First Look

Should you use DLTHub for your ELT usecase?

Businesses produce and accumulate data. Before making sense of this data, we must bring them to a centralized place—a data lake. Whenever you can think of data, movement tools like Fivetran and [Airbyte](data-engineering/airbyte-first-look.md) comes into the picture. As I discussed in the [Airbyte](data-engineering/airbyte-first-look.md) article, the problem with the current ELT ecosystem is that they come with a platform dependency.

One of the main advantage of ELT tools is it's ability to connect different data sources and destination. The platform or language dependency comes in the way of extending/custqomizing the connectors to match your needs.

I've personally faced with problem in more than one occasion

## Problems with ELT Tools

### Airbyte

**Customization**

- Some of the connectors in Airbyte are written in Java. If I have to extend a connector I'll be limited to the language it's written in.

**Open Source??**

- Airbyte is acumilating the market share by using open-source as it's advantage. But they have two different APIs for the open-source and the cloud version. If you try to automate anything with the open-source version, you'll be limited to the API, which is not well documented. Here is my [failed attempt to write a custom Python SDK for Airbyte.](https://github.com/bhavaniravi/airbyte-oss-api-sdk)

### Airflow Providers

**Customization**

My alternative to Airbyte fiasco was to use Airflow without it's platform, just the providers. As you might know the provider ecosystem is huge. All of them are in Python so it's pretty straightforward to extend them.

**Dependency Hell**

But the hope and excitement to use Airflow providers was short-lived. Airflow is known for it's dependency hell. For one, we were using poetry which is not supported. Providers cannot be installed without installing airflow itself. That means I'm brining way too many libraries and it's assoicated constraints into my project and are limited to the version of Airflow I'm using.

## DLTHub

DLTHub was the next ray of hope. It's purely opensource and has no platform dependency. It's all Python and comes with the flexibility of run it anywhere, from your local, server, airflow.

### Installation

Poetry the python dependency manager is something I am heavily using for all my client projects. So support for poetry was a big plus for me. Setting up the dev environment was as simple as running

```
poetry shell
poetry init
poetry add dlt
poetry add "dlt[duckdb]"
poetry add "numpy"
```

### Ease of Use

The example from the documentation is pretty straightforward. I was able to run the example without any issues. Let's start by defining some data

```
data = [
    {'country': 'USA', 'population': 331449281, 'capital': 'Washington, D.C.'},
    {'country': 'Canada', 'population': 38005238, 'capital': 'Ottawa'},
    {'country': 'Germany', 'population': 83019200, 'capital': 'Berlin'}
]
```

Ingest it to duckdb. Why duckdb? because it's inmemory and pretty easy to setup

```
import dlt
pipeline = dlt.pipeline(destination="duckdb", dataset_name="country_data")
info = pipeline.run(data, table_name="countries")
print(info)
```

But it's not ideal to have data as a dict, in realtime it can be from any data source like Github, salesforce or another db. Here is my modified version of the example with reading from duckdb and ingesting it back

```
import dlt
import duckdb

@dlt.resource()
def data():
    # read countries from dlt_main.duckdb
    con = duckdb.connect(database="dlt_main.duckdb")
    for row in con.sql("SELECT * FROM country_data.countries"):
        yield row

pipeline = dlt.pipeline(destination="duckdb", dataset_name="country_data")
info = pipeline.run(data, table_name="countries")

print(info)
```