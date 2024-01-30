---
description: >-
  Decorators are the way to give super powers to your Python functions. It takes
  DRY principle up a notch
---

# Python Decorators - A Deep Dive

A decorator is a function that takes another function as input and returns a function as output. It is one of Python's most powerful features. A decorator can add functionality to a function without modifying the function itself, such as logging, caching, and other functionality.

On the 1st look, decorators are confusing. But, once you understand how they work, you will never write Python code without them. Often times, even people who can't understand the concept of decorators can understand the use cases of decorators.&#x20;

This post has two parts.

1. Understanding the concept of decorators
2. Real-world examples of decorators from famous Python libraries

### What is a function?

If you know a little bit of programming, you know what a function is. Functions encapsulate a piece of code that can be reused.

```python

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

add(10, 20)
sub(20, 10)
```

We all understand this. But do you know functions are objects in Python? Try the following in a Python shell.

```python
print (add)
print (add.__name__)
print (type(add))
print (dir(add))
```

Given this understanding, we can pass functions as arguments to other functions.

```python
def logger(func, *args, **kwargs): # passing function as a argument
    return_val = func(*args, **kwargs)
    print(f'Arguments were: {func.__name__} {args}, {kwargs} and return value was {return_val}')

logger(add, 1, 2)
logger(sub, 1, 2)
```

In the above example, we are passing a `add` as an argument to `logger` and using it to log a variety of things. This intuition of functions' ability to be passed around is the basis of decorators.

### What is a decorator?

A decorator, unlike the above logger function, _should take a function as an argument and return a function_. An updated logger function would look something like

```python
def logger(func):
    def wrapper(*args, **kwargs):
        return_val = func(*args, **kwargs)
        print(f'Arguments were: {func.__name__} {args}, {kwargs} and return value was {return_val}')
        return return_val
    return wrapper

wrapped_add_function = logger(add) # returns a decorated add function
wrapped_add_function(1, 2)
```

Let's take a deeper look at the `logger` function.

1. It takes a function as an argument `func`.
2. Inside that is a function `wrapper` which takes any arg.
3. You can see that the wrapper inner function is returned.
4. The wrapper function is called with the arguments passed to the original function `add(1, 2)`, logs, and returns the value.

### Decorator Syntax

The above example can be written in a more Pythonic way using the decorator syntax. Rather than doing

```python
wrapped_add_function = logger(add)
wrapped_add_function(1, 2)
```

We can simply write

```python
@logger
def add(x, y):
    return x + y
```

Every time you see `@<some-name>` in Python above a function, it is a decorator. The above example is equivalent to

### Decorators with Arguments

The above example is a simple decorator. But what if we want to pass arguments to the decorator? Let's say we want to log only if the function returns a value greater than 10. We can do that by passing arguments to the decorator.

```python

def logger(min_return_val):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return_val = func(*args, **kwargs)
            if return_val > min_return_val:
                print(f'Arguments were: {func.__name__} {args}, {kwargs} and return value was {return_val}')
            else:
                raise Exception(f'Return value is less than {min_return_val}')
        return wrapper
    return decorator

@logger(min_return_val=10)
def add(x, y):
    return x + y

add(1, 2)
```

The above example has 3 functions

1. `logger` - function to register decorator arguments
2. `decorator` - The decorator itself
3. `wrapper` - The wrapper function that runs before and after the original function

#### How does it work?

1. When the code is run, and the interpreter sees `@logger(min_return_val=10)` it actually evaluates the function call. So, it calls `logger(min_return_val=10)` and returns the `decorator` function.
2. The `decorator` function is called with the function to be decorated `add` and returns the `wrapper` function.
3. The `wrapper` function is called with the arguments passed when `add(1, 2)` is called and executes the logic inside the wrapper and `add` function

### Decorators in Famous Python Libraries

For most of my students, the above example doesn't do justice until they go through the following examples. So, let's take a look at some of the decorators in famous Python libraries.

#### Django @login\_required

Django's `@login_required` decorator is used to ensure that a view is only accessible to logged-in users. If an anonymous user requests a view protected by `@login_required`, they are redirected to the login page.

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...
```

[Internally `@login_required` is implemented as a function](https://docs.djangoproject.com/en/3.2/\_modules/django/contrib/auth/decorators/) that takes a view function as its argument and returns a new view function that wraps the original view function. The new view function checks if the user is logged in and, if they are, calls the original view function. If they are not logged in, they are redirected to the login page.

```python
def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
```

#### Flask @app.route

Flask's `@app.route` decorator is used to register a view function for a given URL rule. The view function is called whenever a request with the matching URL is received.

```python
@app.route('/')
def index():
    return 'Index Page'
```

Internally `@app.route` is implemented as a function that takes a URL rule as its argument and returns a new function that takes a view function as its argument and returns a new view function that wraps the original view function. The new view function registers the original view function for the given URL rule.

```python
def route(self, rule, **options):
    def decorator(f):
        endpoint = options.pop("endpoint", None)
        self.add_url_rule(rule, endpoint, f, **options)
        return f
    return decorator
```

You can read my work on [Building your own Flask](https://www.bhavaniravi.com/python/building-own-flask-1) to learn more about how Flask works under the hood.

Similarly, there is `@app.before_request` and `@app.after_request` which are used to register functions to be called before and after each request, respectively.

#### timeit @timeit.timeit

The `@timeit.timeit` decorator is used to time a function. It is used to measure the execution time of a function. This is the most used example to explain decorators.

```python
import timeit

@timeit.timeit
def my_function():
    for i in range(1000000):
        pass
```

The output of the above code will be something like this:

```python
>>> my_function()
0.054
```

If you implement `@timeit.timeit` as a function, it will look something like this:

```python
def timeit(func):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        end = timeit.default_timer()
        print(end - start)
    return wrapper
```

#### Unittest

The `@unittest.skip`, `@unittest.skipIf`, and `@unittest.skipUnless` decorators are used to skip tests. They are used to skip tests that are not applicable in certain situations.

```python
import unittest

class MyTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(mylib.__version__ < (1, 3),
                     "not supported in this library version")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass
```

#### Pytest

My favorite decorator of all time. The `@pytest.mark.parametrize` decorator is used to parametrize tests. It is used to run the same test with different arguments.

```python
import pytest

@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

To understand how `@pytest.mark.parametrize` works, you can read my work on [Building your own pytest](https://www.bhavaniravi.com/python/how-to-build-a-testing-library-like-pytest).

#### Celery

The `@celery.task` decorator is used to create a celery task. It is used to create a celery task from a function.

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def add(x, y):
    return x + y
```

Internally `@celery.task` is implemented as a function that takes a function as its argument and returns a new function that wraps the original function. The new function creates a celery task from the original function.

> This example needs redis to run. You can install redis using `pip install redis`.

#### lrucache

The `@functools.lru_cache` decorator is used to cache the result of a function. It is used to cache the result of a function so that the next time the function is called with the same arguments, the cached value is returned instead of calling the function again.

```python
import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

#### Retry

The `@retrying.retry` decorator is used to retry a function. It is used to retry a function until it succeeds.

```python
import retrying

@retrying.retry(stop_max_attempt_number=7)
def do_something_unreliable():
    if random.randint(0, 10) > 1:
        raise IOError("Broken sauce, everything is hosed!!!111one")
    else:
        return "Awesome sauce!"
```

### Your Turn

I hope that clarifies the concept of decorators. Now it's your turn to try it out. Try to implement the following to understand and make decorators a muscle memory truly.

1. Implement a decorator that handles exceptions on any given function.
2. Implement a decorator that retries a function until it succeeds. Fail after 3 times.
3. Implement a decorator that logs the time taken for a function to run.

Still have questions? Write them to me on [Twitter](https://twitter.com/bhavaniravi\_)
