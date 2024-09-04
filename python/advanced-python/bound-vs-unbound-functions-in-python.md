---
added: Aug 15 2022
description: null
unusedLayout: ../layouts/BlogPost.astro
slug: bound-vs-unbound-functions-in-python
tags:
- advanced-python
title: Bound vs Unbound Functions In Python
---

# Bound vs Unbound Functions In Python

Let's start with a simple Python class Calculator with add method

```python
class Calculator:
    def add(self, numbers):
        pass
```

Now if you do the following, you will see func1 is an Unbound method whereas func2 is an bound method

```python
func1 = Calculator.add
print (func1)

calc = Calculator()
func2 = calc.add
print (func2)
```

You will see the output as following

```
<function Calculator.add at 0x1028e88b0>
<bound method Calculator.add of <__main__.Calculator object at 0x1029fa7c0>>
```

Doesn't say much right? where as if you do the same in **Python2**

```
<unbound method Calculator.add>
<bound method Calculator.add of <__main__.Calculator instance at 0x10470db88>>
```

### Definition

A bound method in Python is the method that has an object associated with it. Unbound method doesn't have an object associated with it. &#x20;

> _The concept of “unbound methods” has been removed from the language as of 3.0. When referencing a method as a class attribute, you now get a plain function object._

If it's removed in 3.0 why should we care?&#x20;

1. It's interesting to see how language features evolve
2. To compare and contrast these behaviors

Let me explain with an example. Try the following code both in Python2 and Python3

```
Calculator.add()
```

Python3 Output

```
add() missing 2 required positional arguments: 'self' and 'numbers'
```

Python2 Output

```
unbound method add() must be called with Calculator instance as the first argument (got nothing instead)
```

**What does this tell us?**

In Python3 unbound methods behave just like mere functions. Does that mean you can pass any random argument to it? Let's try

```
Calculator.add(1, 2)
```

The above snippet doesn't throw any error in Python3 whereas in Python2

```
TypeError: unbound method add() must be called with Calculator instance as first argument (got int instance instead)
```

If it is this helpful, ensures that you aren't playing around passing random arguments why did they remove it?

### Why did Python3 Remove Unbound Methods?

Internet talks very little about why the unbound method was removed. [Gudio himself](https://python-history.blogspot.com/2009/02/first-class-everything.html) gives us an idea in his blog

If you run the following snippet in Python2 it will throw an error exactly as above. Whereas Python3 doesn't

```
class Foo(object):
  def bar(self):
    self.val = 2
    return self
    
class O(object): 
    pass
    
Foo.bar(O()).val # returns 2
```

This is called **"**_**Duck typing self"**_&#x20;

### Duck Typing Self

Duck-typing-self is the concept of defining the type of self dynamically at run time rather than restricting that it should be bound to the particular class type. In the above snippet, there is no Foo's bar function is called with a random object O

> It is important to note that the **"**_**Duck typing self"**_  is a side effect of removing unbound method and not the core reason

I asked the same on reddit, let's hope to find some answers

{% embed url="https://www.reddit.com/r/Python/comments/wokoow/why_were_unbound_methods_removed_in_python3/?context=3&utm_medium=web2x&utm_source=share" %}