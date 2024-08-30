---
added: Aug 04 2022
description: null
layout: ../layouts/BlogPost.astro
slug: how-to-do-code-reviews
tags:
- software-engineering
title: How to Do Code Reviews?
---

# How to Do Code Reviews?

### Code Quality

* Define what a good PR is and ensures that the PR adhers to it
* You can add a PR checklist template to remind people of the ettiquties of the project
* Does the PR justify the feature, is it making a single atomic change to the system. PR that changes a million things will become hard to track and manage
* Check the functionality. The very reason to do reviews is to get an outside eyes on the functionality. Mentally check for any corner cases missed
* Is the code readable, changeable and maintainable?
* Is the code following the construts of the language? Often times newbies tend to stick to patterns of language they learned first. _For example in Python using list comprehension over updating a list inside a for loop_
* Is the code documented well?
* Are there enough testcases to cover the newly introduced logic?
* Does the new code follow the design guidelines of the project? If you don't have a guideline it is a good idea to create one and communicate it to the team
* If a comment is repeated across multiple team members then add it to your guideline and communicate it with your team

### People

* Ensure you are addressing the problem not the person
* Explain in detail what you think, give a full picture to the author instead of empty comments like "It won't work"
* Quote things that you like. Code reviews are not just for finding mistakes but also to learn from. If you found something good/useful/interesting communciate.
* Review your code yourself first. Add comments, fix them. This will ensure the author knows that you've made your best effort.

### What to Avoid?

* Ensure you don't use PR as a playing field for new ideas. If you get a new idea to improve the interface create it as an issue.
* Don't make too many changes, split larger issues/features into smaller ones and raise a PR
* PRs hang in for review are a huge bottleneck. We all are busy at our own work but make time every week to review. If you don't have time to review your teams' PR take to your manager
* Not doing code review itself
* Don't take PR comments personally. Reviews are for your code not you, when it is directed at you or your skills take it up with your manager. It's not OK.

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}