---
added: Aug 13 2022
description: null
layout: ../layouts/BlogPost.astro
slug: can-next-scheduled-run-automatically-re-run-failed-task
tags:
- apache-airflow
title: Can Next Scheduled Run Automatically Re-Run failed Task?
---

# Can Next Scheduled Run Automatically Re-Run failed Task?

No and Yes.

No Airflow doesn't support it as a feature out of box

But you can use APIs and structure your dag in such a way to make this possible

Here is how I would go about it

1. Add a task at the start of the pipeline
2. In this task query the last-1th dagrun. The last dagrun is the current one
3. Get all the failed task from that dagrun
4. Clear their state

**Idempotency**

* Ensure all your tasks are idempodent ie., doesn't matter how many times a task is ran it takes the same set of input and arrives at the same set of output
* This means if a task fails inserting 100th row, it should be able to revert back and reinsert them when cleared

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}