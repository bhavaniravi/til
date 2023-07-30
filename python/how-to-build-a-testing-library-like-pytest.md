---
description: >-
  As Pythonistas, we all love Pytest. No questions there. But what if we embark
  on a journey of building something similar on our own?
---

# How to Build a Testing Library Like Pytest?

### Introduction

Let's talk about a skill that every developer dreams of mastering - writing unit tests. We all know that testing is the secret sauce that makes our code rock-solid and dependable. And when it comes to the Python world, pytest is practically our code-testing deity! 🙌

But wait, have you ever wondered how pytest works under the hood? Sure, you can find a gazillion tutorials on how to use it, but let's take a different route. In this blog, we'll embark on an exciting journey to build our testing library from scratch.

### Pytest 101

If you have never seen pytest before, I don't want to throw you under the bus.

```
app
|__ tests
    |__ test_calculator.py
|__ calculator.py
```

Now you install pytest

```
pip install pytest
```

Run pytest

```
pytest
```

Now all tests in the `tests` folder runs. A sample test case can look like this

```python
from app.calculator import add

def test_add():
    assert add(2, 3) == 5
```

### Other Pytest Features I love

#### Parametrized Test Cases

```python
@pytest.mark.parametrize("test_input,expected", [
    ([2, 3], -1),
    ([3, 2], 1),
    ([5, 5], 0),
])
def test_subtract(test_input, expected):
    assert subtract(*test_input) == expected
```

#### Fixtures

Fixtures come in handy when you want to set up and teardown some resources before and after a test case. For example, you want to set up a database connection before a test case and teardown after the test case.

```python
@pytest.fixture
def setup():
    print("Setup")
    yield
    print("Teardown")

def test_fixture(setup):
    print("Test")
```

#### Check for exceptions

```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

### Why this? Why Now?

Wonderful, now let's take all these features as our inspiration to try and build our own.

1. Why do this? For fun, because we can :P
2. _What I cannot build, I do not understand - Richard Feynman_
3. It's fun. I told you that I already.

Can't Copilot do this for me? No, since there are no code examples like this except for the pytest source code itself. But when I tried specific cases like Fixtures, the results were good to draw inspiration from.

**Disclaimer: This is an experiment never meant to see production or usage. The code doesn't resemble pytest. Infact, all my attempts to read the pytest code went down the drain. This is purely my version**

### Features of a  Testing Library

### Test Runner

* Find all test files and test functions

```python
for dr in os.listdir(sys.path[0]):
    if dr != "tests":
        continue
    for files in os.listdir(dr):
        if not (files.startswith("test") and files.endswith(".py")):
            continue
        module = importlib.import_module(dr + "." + files[:-3])
            for members in getmembers(module, isfunction):
                if members[0].startswith("test"):
```

* calling the test functions, i.e., calling the test function

```python
try:
    members[1]()
except AssertionError as e:
    errors[members[1]] = e
```

* Capture all test results (success, failure, error)

```python
for member, ex in errors.items():
        tb = ex.__traceback__
        while tb is not None:
            if tb.tb_next is None:
                break
            tb = tb.tb_next

        trace = []
        trace.append(
            {
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno,
                "traceback": traceback.format_tb(tb),
            }
        )
        print(type(ex).__name__, trace)
```

### Parametrized test cases

* create `owntest.parametrized` function. We all know it's a parametrized decorator

```python
def parametrize(keys, values):
    def decorator(func):
        def wrapper():
            ...
        return wrapper
    return decorator
```

* Let's preserve the parameters

```python
Input
# keys = "test_input,expected"
# values = [("3+5", 8), ("2+4", 6), ("6*9", 54)]

Output
# params = [{"test_input": "3+5", "expected": 8}, {"test_input": "2+4", "expected": 6}, {"test_input": "6*9", "expected": 54}]
```

```python
def parametrize(keys, values):
    def decorator(func):
        params = []
        for value in values:
            param = {}
            for i, key in enumerate(keys.split(",")):
                param[key] = value[i]
            params.append(param)
```

* Run parametrized test cases, with each parameter

```python
def wrapper(*args, **kwargs):
    """Runs the original test function with multiple params"""
    for i, param in enumerate(params):
        print("subtest running", i + 1)
        func(**param)
```

### Fixtures

Let's create `owntest.fixture` function. This decorator will store the fixture function in a dictionary. Later when we run the test, we can map the function attribute names to a fixture.

#### Register Function as Fixture

```python
def fixture(function):
    def fixture_wrapper():
        return function()

    return fixture_wrapper
```

#### Create a map of Fixtures

* Update the test runner to run fixtures

```python
for members in getmembers(module, isfunction):
    if "fixture_wrapper" in members[1].__name__:
        fixtures_mapping[members[0]] = members[1]
```

#### Handling Test Argument that is a Fixture

If the recognized function is a fixture, as stored in fixture mapping, check if the function is a generator. If yes, generate the value with `__next__` else use the return value directly on the test function

```python
for arg in members[1].__code__.co_varnames:
    if arg in fixtures_mapping:
        fixture_return_value = fixtures_mapping[arg]()
        # check if the generator
        if hasattr(fixture_return_value, "__next__"):
            func_args.append(next(fixture_return_value))
        else:
            func_args.append(fixture_return_value)
```

\
And that wraps up our adventure into the world of building a testing library in Python! We've covered all the essential components - test discovery, functional test cases, fixtures, and parametrized test cases - that come together to create a fantastic testing framework.

Now armed with this newfound knowledge, you have the tools to craft your very own testing library customized to suit your project's needs. It's an exciting journey that lets you showcase your coding prowess while ensuring your code is thoroughly validated.

So, go ahead and take on the challenge and rebuild owntest in your own way. Maybe think about testing your testing library.&#x20;

Until my next freaky experiment, see ya.

I will be presenting this post as a talk at [Pycon AU 2023](https://2023.pycon.org.au/program/D9TMCM/). If you are around, say hi.
