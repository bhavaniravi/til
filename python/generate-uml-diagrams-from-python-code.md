---
title: How to Generate UML Diagrams from Python Source Code?
sub_title: Add UML diagrams along with every version of your code
slug: generate-uml-diagrams-from-python-code
tags: ["python"]
featuredImgPath: https://i.imgur.com/iWtiiYx.png
isexternal: true
published_date: 2021-10-13
created_date: 2021-10-12
description: Trust me code moves faster than the digrams that you created
  for   the documentation. How about a Python tool that you can add to your
  CI/CD   pipeline that generates UML diagram for each version of your code?
draft: false
---
# Generating UML Diagrams from Python Code

The Unified Modeling Language is a general-purpose, developmental, modeling language in the field of software engineering that is intended to provide a standard way to visualize the design of a system.

Inspite of designing and thinking through the class structure before coding, developers might have to restructure and refactor the code during implementation. It is also a good idea to generate UML diagrams from code and see if it matches the actual design. 

## Pyreverse

Pyreverse is a set of utilities to reverse engineering Python code. It uses a representation of a Python project in a class hierarchy which can be used to extract any information (such as generating UML diagrams or unit tests, as pyargo and py2tests). 

The package is now a part of `pylint` so to install it you need pylint installed in your python environement.

```
pip install pylint
```

## Generating Diagrams

1. Let's choose a project, feel free to choose any python project of your choice

```
git clone <python requests>
```

2. Create a python virtualenv with pylint installed. Activate the environment.

```
pip install pylint
```

3. Use `pyreverse` command to create the UML diagram image

```
pyreverse -o png <path_to_src>
```

The generated image looks something like this.

<figure>

![](https://i.imgur.com/ucWHkb5.jpg)

</figure>

