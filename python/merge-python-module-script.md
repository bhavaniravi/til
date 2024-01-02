---
title: Merging Python Modules
sub_title: how to write a python script to merge multiple python modules into single one
slug: merge-python-module-script
tags:
  - python
featuredImgPath: https://i.imgur.com/gine5et.png
isexternal: true
published_date: 2022-01-29T00:00:00.000Z
created_date: 2022-01-29T00:00:00.000Z
draft: false
description: >-
  Airflow had many AWS providers that weren't following the latest conventions.
  The resolution involes merging multiple modules into single Python file. I
  wrote this script to automate the task.
---

# Merging Python Modules

Recently I took up the humongous task of Merging multiple Python modules into a single one for Apache Airflow. Airflow has many AWS providers that weren't following the latest conventions. So with issues [#20139](https://github.com/apache/airflow/issues/20139) and [#20296](https://github.com/apache/airflow/issues/20139) we set out to resolve it.

What waited ahead was a line up of PRs which involves

1. Create a new Python module
2. Add the license agreement to it
3. Move all the classes from independent modules to the new one
4. Add imports from each independent module
5. Add deprecated warning block to old modules
6. Fixing all the imports in test cases and examples

As you can see, this task soon became quite repetitive since we were dealing with different AWS products like EMR, EKS, EC2, DMS, etc., Overtime the process got boring and icky, and I did what any developer would do. Automated it. Along the way, I also learned quite a few things.

## Reading all the top-level imports

A typical Python module can contain a variety of stuff. Imports, Global variables, functions, lambdas, but in this case, it was imports and classes. The first task is to load these imports and classes' source code into Python objects written to the new module.

```
imports = []
classes = []
class_names = []
```

The ast module came in handy to load the Python module and load it into a tree. This is my first time with ast, and pretty amazed by what it can do. So buckle up

```
def get_imports(path):
    with open(path) as fh:
       root = ast.parse(fh.read(), path)
```

Next, we loop through these nodes and capture classes and imports.

```
for node in ast.iter_child_nodes(root):
    if isinstance(node, ast.Import):
        module = []
    elif isinstance(node, ast.ImportFrom):
        module = node.module.split('.')
```

In the case of an import statement, there are variations.

```
import math
from datetime import datetime
import datetime as dt
```

We construct the import strings on the fly and have them handy to handle all of this.

```
for n in node.names:
    if not module:
        statement = f"import {n.name}"
    else:
        statement = f"from {'.'.join(module)} import {n.name}"
        if n.asname:
            statement = statement + f"as {n.asname}"

    imports.append(statement)
```

## Get Classes' source code

Let's shed some more light on the code section that captures the classes and their source code. I used a library called `astunparse`, which unparses an ast node back to its source code form.

```
for node in ast.iter_child_nodes(root):
    ...
    ...
    elif isinstance(node, ast.ClassDef):
        class_names.append(node.name)
        source = astunparse.unparse(node)
        classes.append(source)
        continue
```

The `astunparse` [module](https://github.com/simonpercivall/astunparse/blob/2acce01fcdda2ea32eea835c30ccca21aaff7297/lib/astunparse/unparser.py#L59) has a `dispatch` method which walks through the ast and unparses the node based on its type.

## In the future

The current script is pretty limited in its capabilities. I'm not going to work on them until a need arises.

1. It will work only on modules' import statements and classes. Any other python construct will be ignored
2. Unparse makes all docstrings a single line with with single quotes.
3. The current script does not handle multiple imports.

***

The snippet, along with an example directory, is available in my [github repository](https://github.com/bhavaniravi/mergepy/tree/main)

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
