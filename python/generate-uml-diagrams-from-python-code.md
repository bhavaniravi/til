---
title: How to Generate UML Diagrams from Python Source Code?
sub_title: Add UML diagrams along with every version of your code
slug: generate-uml-diagrams-from-python-code
tags:
  - python
featuredImgPath: https://i.imgur.com/iWtiiYx.png
isexternal: true
published_date: 2021-10-13T00:00:00.000Z
created_date: 2021-10-12T00:00:00.000Z
draft: false
description: >-
  Your code moves faster than the digrams you created for the documentation. How
  about a Python tool that you can add to your CI/CD pipeline that generates UML
  diagram for each version of your code
---

# How to Generate UML Diagrams from Python Source Code?

Inspite of designing and thinking through the class structure before coding, developers might have to restructure and refactor the code during implementation. It is also a good idea to generate UML diagrams from code and see if it matches the actual design.

## Pyreverse

Pyreverse is a set of utilities to reverse engineering Python code. It uses a representation of a Python project in a class hierarchy which can be used to extract any information (such as generating UML diagrams or unit tests, as pyargo and py2tests).

The package is now a part of `pylint` so to install it you need pylint installed in your python environement.

```
pip install pylint
```

{% @mailchimp/mailchimpSubscribe cta="Never miss a Python article. No spam!" %}

## Generating UML Diagrams

1. Let's choose a project, feel free to choose any python project of your choice

```git
git clone <python requests>
```

2\. Create a python virtualenv with pylint installed. Activate the environment.

```bash
pip install pylint
```

3\. Use `pyreverse` command to create the UML diagram image

```bash
pyreverse -o png <path_to_src>
```

[The generated image looks something like this.](https://i.imgur.com/ucWHkb5.jpg)

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>
