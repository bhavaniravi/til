---
added: Nov 16 2022
draft: false
image: null
unusedLayout: ../layouts/BlogPost.astro
slug: python-generators-vs-iterators
sub_title: Generators and Iterators are Python constructs that lets you loop through
  data in chunks instead of loading them into memory. This post discusses the subtle
  differences between them
tags:
- advanced-python
title: Python Generators vs Iterators
---

# Python Generators vs Iterators

In Python, both generators and iterators ensure data is not loaded into memory on the whole but rather processed chunk by chunk. But when to use a generator and iterator.

### What is a Generator?

A generator is a Python function that `yeild` a result. Every generator is an iterator. A generator function returns a generator object

```python
def generate(n):
    for i in range(n):
        yield i
```

```python
x = generate(3)
print (x)
print (next(x))
print (next(x))
print (next(x))
print (next(x)) # raises StopIteration
```

### What is an Iterator?

An iterator is a Python object which returns an iterable via `__iter__` method. An iterable has `__next__`

[Python Iterators and Iterables](https://thelearning.dev/python-iterables-and-iterators) talks about iterators in detail, but for now, let's look at a simple example

```python
class GenerateN:
    def __init__(self, n):
        self.n = n
        self.i = -1
        
    def __iter__(self):
        return self
        
    def __next__(self):
        self.i += 1
        return self.i
```

```python
g = GenerateN(3)
print (g)
print (next(g))
print (next(g))
print (next(g))
print (next(g)) # raises StopIteration
```

### When to use a Generator vs. an Iterator?

* Generators are function, and Iterators are object-oriented.
* Use generators when you have a large stream of data and you want to loop over them.
* Use iterators to generate a sequence of data.
* Generators are excellent for large loops since it only works on one value at a time.