---
added: Nov 16 2022
draft: false
image: null
unusedLayout: ../layouts/BlogPost.astro
slug: what-is-__name__-__main__-in-python
sub_title: Python snippets use __name__ == "__main__" checks to ensure that the module-specific
  code is ran only when they are run directly via Python. Let's see that with an example
tags:
- python
title: What is \_\_name\_\_ == "\_\_main\_\_" in Python?
---

# What is \_\_name\_\_ == "\_\_main\_\_" in Python?

If you are a Python beginner, you often see `if __name__ == '__main__'` and get confused about what it does. You are not alone. Most of my students at #PythonToProject Bootcamp struggle with this as well.

The `if __name__ == '__main__':` ensures that the snippet under it gets executed only when the file is run directly.

### Running Python module

```python
# app.py

print ("app.py __name__=", __name__)

if __name__ == '__main__':
    print ("inside main check block")
```

When you run this code `python app.py` you will get the following output

```
app.py __name__=__main__
inside main check block
```

### Importing Python module

Whereas if you import `app` into another module

```python
# temp.py
import app

print ("temp.py __name__=", __name__)
```

The output will be

```
app.py __name__=app
temp.py __name__=__main__
```
