---
title: Are your Secrets Safe In Python?
sub_title: Storing your secrets as Python file, here is what you need to be aware of
slug: secrets-as-python-file
tags:
  - python
featuredImgPath: https://i.imgur.com/9lCN0V6.png
isexternal: true
published_date: '2020-05-14'
created_date: '2020-05-14'
draft: false
description: >-
  Secrets and token stored as Python config or secrets file has a chance of
  being exposed via pyc files when commited to GitHub repository
---

# Are your Secrets Safe In Python?

On scrolling through Hackernews, I stumbled upon this article where [Jesse](https://twitter.com/\_\_jesse\_li) points out how you or your organization can have [secrets hidden in the form of `pyc` files](https://blog.jse.li/posts/pyc/).

While Jesse's code has scrolled through Github repos and intimated the code owners, there is a good chance that our private repo could have some hanging around.

I modified the code to scroll through Saama's private repositories. Gladly I didn't find any `pyc` files checked in.

You can use the same code to scroll through your private repositories.

## Dependencies

```
pip install PyGithub
pip install uncompyle6
```

### Code

If you want to jump ahead to the whole code checkout [the Github repo](https://github.com/bhavaniravi/pyc\_secrets)

1. Import necessary packages

```
import base64
import io
import os
import tempfile
import uncompyle6
from github import Github
```

1. Authenticate with Github

Create a private access token and use it to authenticate yourself

```
GITHUB_KEY = <GITHUB_ACCESS_TOKEN>
g = Github(GITHUB_KEY)
```

1. Get all repos given an organization

```
repos  = g.get_organization(<ORGANIZATION>).get_repos(type="private")
```

1. Find files with \*.pyc extension

```
for repo in repos:
    print (repo)
    try:
        contents = repo.get_contents("")
    except:
        continue
    for file_ in contents:
        try:
            extension = file_.name.split(".")[1]
        except IndexError:
            extension = None
        if file_.name in secrets or ( extension and extension  == "pyc"):
            items.append(file_)
```

1. If there are no `pyc` files, you are good to go

```
if not items:
    print ("No files found, you are good!")
```

1. If any `pyc` files might contain secrets decompile and print them out

```
for item in items:
    print(f"DECOMPILING REPO https://github.com/{item.repository.full_name}")
    print(f"OWNER TYPE: {item.repository.owner.type}")
    try:
        contents = base64.b64decode(item.content)
        with tempfile.NamedTemporaryFile(suffix=".pyc") as f:
            f.write(contents)
            f.seek(0)

            out = io.StringIO()
            uncompyle6.decompile_file(f.name, out)
            out.seek(0)
            print(out.read())
    except Exception as e:
        print(e)
        print(f"COULD NOT DECOMPILE REPO https://github.com/{item.repository.full_name}")
        continue
    print("\n\n\n")
```

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
