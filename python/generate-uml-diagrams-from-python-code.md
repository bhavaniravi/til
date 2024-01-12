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

In spite of designing and thinking through the class structure before coding, developers might have to restructure and refactor the code during implementation. It is also a good idea to generate UML diagrams from code and see if it matches the actual design.

I've explored a variety of [code diagram generators](uml-isnt-dead.md), and the one that stood out for me was a  Pyreverse example

## [Pyreverse](https://pypi.org/project/pylint/?utm\_source=bhavaniravi.com\&utm\_medium=website\&utm\_campaign=bhavaniravi-uml\&utm\_id=uml-diagrams)

Pyreverse is a set of utilities to reverse engineering Python code. It uses a representation of a Python project in a class hierarchy which can be used to extract any information (such as generating UML diagrams or unit tests, such as pyargo and py2tests).

The package is now a part of [`pylint`](https://pypi.org/project/pylint/?utm\_source=bhavaniravi.com\&utm\_medium=website\&utm\_campaign=bhavaniravi-uml\&utm\_id=uml-diagrams) so to install it. You need pylint installed in your python environment.

```
pip install pylint
```

## Generating UML Diagrams

1. Let's choose a project; feel free to choose any python project. I'm using Python requests library's source code

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

The generated image looks something like this. (Click to open)

<figure><img src="../.gitbook/assets/image (6) (1).png" alt=""><figcaption></figcaption></figure>

***

{% embed url="https://bhavaniravi.substack.com/embed" fullWidth="true" %}
Newsletter embed
{% endembed %}
