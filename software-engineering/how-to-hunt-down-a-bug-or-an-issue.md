---
added: Apr 30 2023
draft: false
image: null
layout: ../layouts/BlogPost.astro
slug: how-to-hunt-down-a-bug-or-an-issue
sub_title: It's not working. It gives an error. How to resolve a bug or an infra issue
  without losing it
tags:
- software-engineering
title: How to hunt down a bug or an Issue
---

# How to hunt down a bug or an Issue

1. Find out what the error is. It can manifest in different ways. Sometimes it's an error traceback; sometimes a network call not propagating through, and sometimes a pod crashing repeatedly.
2. Look one level deeper Whatever way the error manifests, look into it, like really look into it.
3. If it is a traceback, figure out which library is causing it
4. If it's a network call, understand the path it can potentially take before reaching the respective server
5. If it's an pod not start look at logs, events,&#x20;
6. Sometimes the errors are generic that's when you take a step back and get a 360 degree view of all systems involved
7. Questions to ask yourself
   1. Have I seen this before - Life is easy peasy
   2. Have I seen something like this before
8. Searching the internet
   1. A simple google search&#x20;
   2. Github issues
   3. Community forums
9. Experimentation
   1. Based on the above notes come up with a series of hypothesis for the potential causes of the issue
   2. Devise a way to test them. Sometimes it's entering the prod system and running some scripts, sometimes it's changing some configuration
   3. Different error is progress, know when you're complicating the issue v
10. Communicate
    1. People like answers not process
    2. But it is better to communicate that what you're doing is an experimentation
11. Feelings
    1. Some issues have the power to take over you
    2. Like 24/7 process
    3. Take break
    4. Talk to someone
    5. Rubber duck your processs
12. Writing/Bug report
    1. Revisit your notes
    2. Answer the damn question
    3. Add details later
13. Why should every software engineer do production support?
    1. Understand the needs of the customer
    2. Understand the system beyond the context of their development
    3. Trains your brain to work through the issues quicker
14. Debugging a Github action
    1. Debug the steps
    2. Local system has aws creds
    3. Work with env variables
15. Debugging Databricks with Airflow
    1. The wrong variable unsupported
16. What can you do as a software engineer
    1. Write better error messages
    2.