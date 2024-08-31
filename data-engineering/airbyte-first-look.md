---
added: May 24 2023
created_date: '2023-06-30'
description: Businesses produce and accumulate data. Before making sense of this data,
  we must bring them to a centralized place—a data lake. Whenever you can think of
  data, movement tools like Fivetran comes into the picture. Airbyte is an ELT(Extract,
  Load, Transform) accumulating its market of Fivetran by using open source to its
  advantage.
draft: false
featuredImgPath: null
image: null
isexternal: true
layout: ../layouts/BlogPost.astro
published_date: '2023-07-07'
slug: airbyte-first-look
sub_title: Should you use Airbyte for your ELT usecase?
tags:
- data-engineering
title: Airbyte - First Look
---

# 🔗 Airbyte - First Look

Should you use Airbyte for your ELT usecase?

Businesses produce and accumulate data. Before making sense of this data, we must bring them to a centralized place—a data lake. Whenever you can think of data, movement tools like Fivetran comes into the picture.

Airbyte is an ELT(Extract, Load, Transform) accumulating its market of Fivetran by using open source to its advantage.

It's not just the open source that makes Airbyte so special. It's also the features and its ecosystem. Let's learn more about it.

<div>

<figure><img src="https://hackmd.io/_uploads/B1vvxkoB2.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screenshot 2023-05-24 at 6.24.47 AM.png" alt=""><figcaption><p>Airbyte illustration</p></figcaption></figure>

</div>

### [Connectors](https://docs.airbyte.com/integrations)

#### Source connectors

Airbyte has 300+ source connectors.

You have the option to pull data from 300 different sources. Starting from storage like S3, and GCS to Databases like Postgres and Snowflake to Apps like Hubspot and Salesforce

#### Destination Connectors

Airbyte has 30+ destination connectors.

That might sound like a small number, but that is good enough to solve most of the ELT use cases. Companies primarily use ELTs to bring data to a centralized data lake. Airbyte supports Postgres to Bigquery to Snowflake for this purpose.

#### Is it like Zapier?

Now another question might arise if there is a source and destination. Is it like Zapier? Please be noted, Zapier is a trigger/event-based system and not a data-loading system. Zapier triggers action at the destination if the source condition matches.

Airbyte, on the other hand, will move your data from one system to another

#### Can I add a custom connector?

Yes, you can. You can write custom connectors in Python or Java. There is a Connector Development kit(CDK) that generates basic templates for you to fill in later.

#### Can I customize an existing Connector?

That part is a little tricky. Yes, and a No. Since you can build custom connectors in Python or Java, the extensibility of an existing connector depends on which language it's written in and which language you are extending it to

### [License](https://docs.airbyte.com/project-overview/licenses/license-faq#airbyte-licensing-overview)

Airbyte has a managed service with a separate Enterprise license. But, I was only concerned about open source. Airbyte connectors/protocol/CDK are under **MIT License**. Airbyte core uses **ELV2**. That means you cannot sell Airbyte as a hosted service to your customers.

Let's not get into this really open-source debate here. You can use Airbyte for your commercial purposes as long as you're not selling the hosting itself as a service.

### Usecase

When looking for ELT systems, we look for a few things

- Has enough connectors to pull/push data ✅
- Can run full-load or incremental data ✅
- Can run on schedule ✅
- Scale ✅
- Error management/Notifications ✅
- Configurable Resource management ✅

### [Setup and Usage](https://docs.airbyte.com/cloud/getting-started-with-airbyte-cloud)

If you want to try Airbyte locally, It is pretty easy to set up. You clone the Airbyte repo and run a script. Airbyte spins up several Docker containers and prepares your app for use.

<figure><img src="../../.gitbook/assets/upload_ecc12e163aa72e584f24f8a9148cb5bd.png" alt=""><figcaption><p>Airbyte UI with connection configured</p></figcaption></figure>

### [Documentation](https://docs.airbyte.com/cloud/core-concepts)

The core documentation is pretty clear. You can grasp the concepts like source, destination, streams, CDC and the architecture, metadata db

The source and destination are vast, and the quality of its documentation can only be assessed by the one with specific domain knowledge.

The learning curve might be steep if you aren't aware of data engineering concepts. But that shouldn't stop you.

### Moving Pipelines to Production

After you set up Airbyte and try moving data from source to destination, an alarming reality hits. Wait a minute! Everything I have done so far is in UI in my local. How am I going to move it to prod?

That's where Airbyte's [Octiva CLI](https://docs.airbyte.com/cli-documentation) comes in handy. Octiva CLI lets you export/import your sources and connections. `octiva export` will give you a YAML file, which can be applied again

\---

```
Buckle up as we are entering not-so-good parts
```

### Performance

This is a WIP. From whatever I have run in the system. I would call it slow. A few old Reddit threads agree.

### Community and Support

- I have mixed views on this. Stackoverflow has just 75 questions
- Airbyte Slack has about 13K members. There is a bot called kapa.ai that answerers questions. But I might be biased here. The questions are not cross-answered. In Airflow Slack, the community helps each other out when there is a question. This is something that the Airbyte community has to develop

### Customization

- This is where I find the major drawback, maybe because I come from Airflow(Python) world.
- The connectors are developed in Python/Java. Most of the configuration is YAML based.
- To version control existing connectors, you must use Octiva cli to export YAML files.
- One drawback is that you cannot extend these connectors for customization.

### API

This is something I'm frowning upon because the OSS API is different from their platform API. Though both are documented, the OSS API ought to change and has no support. The open-source API does not have an SDK.

I quickly thought I could hack my way around it by building a think SDK layer. Still it became a bottomless pit of undocumented JSON schema for different source/destination connectors.

### Credentials management

Airbyte stores the credentials of your sources/destination either in a database or secret manager. Currently, there is only support for Google secret manager.

This is one of the major cons for me. Because most companies have a centralized cred management system, e.g., Hashicorp or AWS, this feature is a WIP in Airbyte OSS.

Another disadvantage is companies often have a secret manager in place. You can't just plug it in and call it a day. I have to configure it all again via Airbyte UI.

### Would I still use it?

#### **Yes**.

If the use case is straightforward to pull data from different sources.

If it's integrating with a different system or involves a lot of customization, you're better off building your own.

Overall, for a product that's only three years old. Airbyte is doing all the right things and will continue to do more.