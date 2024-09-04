---
added: Mar 16 2023
draft: false
image: null
unusedLayout: ../layouts/BlogPost.astro
slug: python-position-and-keyword-only-arguments
sub_title: What does / and * mean in a Python function definition mean
tags:
- advanced-python
title: Python Position and Keyword Only Arguments
---

# Python Position and Keyword Only Arguments

Recently when I was teaching PythonToProject bootcamp, one of my students had a question about Python's `__new__` function. `__new__` The function lets you manipulate how you create your objects. That wasn't what caught my eye.

We all know about `*args` and `**kwargs` in function calls. But have you seen something like these

```
def new_function(x, /, y, z):
    pass
    
def new_function_1(x, y, z, *, scale):
    pass
```

You can use the `help` method to understand any object, class, or function in Python. To show my students that \_\_new\_\_ and \_\_init\_\_ are default constructs that are available even in builtin classes like `int` or `float` I ran the following in the Python shell

<pre class="language-python"><code class="lang-python">help(int) # will show that int is a class 
<strong>
</strong>
help(int.__new__) # will show that a __new__ method exists
>>> help(int.__new__)

Help on built-in function __new__:

__new__(*args, **kwargs) method of builtins.type instance
    Create and return a new object.  See help(type) for an accurate signature.
(END)
</code></pre>

When I ran it for `__init__`

```
help(int.__init__) # BOOM! I learned something new. 

Help on wrapper_descriptor:

__init__(self, /, *args, **kwargs)
    Initialize self.
```

Did you see it yet?

The `__init__(self, /, *args, **kwargs)` line. What is that `/` doing in the middle of the function definition? You can also replace `/` it with `*` and these are two new features introduced in 3.8

### Position Only Arguments

To enforce that a function accepts certain arguments only based on their position and not by their name, you mention them in the function definition and follow it up with a `/.`All arguments following the `/` can be positional or keyword based

A good use case for this is cases where the position of the argument means something.&#x20;

```
def point(x, y, z, /, scale=1):
    pass
```

For the above function, if you pass `point(x=10, y=20, z=30)` will raise an error

```

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: point() got some positional-only arguments passed as keyword arguments: 'x, y, z'
```

Here is a bonus example for you.

```
def rgb_to_hex(r, g, b, /):
    pass
```

### Keyword Only Arguments

Similarly, you can enforce a function to pass keyword-only args by prepending the list of args with a `*` -[PEP3102](https://peps.python.org/pep-3102/)

All arguments before the `*` can be positional. Python's sorted method is a wonderful example for this. It uses both keyword and positional args.

```python
def sorted(iterable, /, *, key=None, reverse=False)
    ...
```

When you pass keyword-only args as positional args, the function will behave as if an unknown argument is passed

```python
x = [1, 2, 3]
sorted(x, True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: sorted expected 1 argument, got 2
```

Whereas when you do&#x20;

```python
sorted(x, reverse=True)
[3, 2, 1]
```



\---&#x20;

Next time when you write an function and want to enforce the users to use position or keyword based arguments, you know how to implement it.