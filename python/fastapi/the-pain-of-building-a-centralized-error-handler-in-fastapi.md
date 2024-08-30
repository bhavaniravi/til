---
added: Sep 06 2023
description: null
layout: ../layouts/BlogPost.astro
slug: the-pain-of-building-a-centralized-error-handler-in-fastapi
tags:
- fastapi
title: The Pain Of Building a Centralized Error Handler in FastAPI
---

# The Pain Of Building a Centralized Error Handler in FastAPI

**Disclaimer 1**

> 100% human, 0% chatgpt

**Disclaimer 2**

> The blog contains code snippets and error logs, it's better you follow along by spinning up the respective code.

All the code used in this blog post can be used here [https://github.com/bhavaniravi/fastapi-centralized-exception-handler-demo](https://github.com/bhavaniravi/fastapi-centralized-exception-handler-demo)

I have been using FastAPI for almost five months extensively. Every day, I wake up to writing new APIs and test cases for our business function. The project is growing day by day, and we wanted to have a centralized error handler.

This blog post covers the hurdles I faced while implementing it and how I overcame them.

### Setting the Stage

To walk through this experiment with me, you need a FastAPI app. Let's call this project `Playground` and our custom exception will be the Playground Exception

```python
# exception.py


class PlaygroundError(Exception):
    def __init__(self, message, http_code):
        self.message = message
        self.http_code = http_code
        super().__init__(message)
```

The FastAPI app will look something like this.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    raise PlaygroundError("exception raised", 400)
    

@app.get("/divide")
def divide():
    return 1 / 0 # raises zero division error
```

To handle these errors in a centralized fashion throughout the project, there is a hook in FastAPI to plugin a function

```python
async def playground_exception_handler(request, exc):
    print ("playground exception handled")
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message},
    )
    
@app.add_exception_handler(PlaygroundError, playground_exception_handler)
```

You can also handle the `ZeroDivisionError` the same way.

```python
async def handle_exception(request: Request, exc: Exception):
    print ("handler for generic exception")
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )
    
app.add_exception_handler(ZeroDivisionError, handle_exception) 
```

When you run the application with `uvicorn app:app --reload` and hit the API `localhost:8000/` you will get a nicely formed JSON response with the error message and http status code 400.

Looks nice, easy, and simple, right? What's the problem?

### Introducing Background Tasks

The project I was working on predominantly used background tasks to run the business logic. Given large data processing.

When an API throws an error in the background, the process `exception_handler` hook no longer catches them. Because by the time the exception reaches, the response is already generated.

Don't trust me? Try this.

```python
async def background_task():
    raise PlaygroundError("custom error", 3000)


@app.get("/background")
def background(bg: BackgroundTasks):
    bg.add_task(background_task)
    return {"message": "Hello World"}
```

Now, when you hit this API with a background task `localhost:8000/background` You will receive a `RuntimeError` traceback.

```bash
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
    await self.app(scope, receive, sender)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
    raise e
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/routing.py", line 718, in __call__
    await route.handle(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/routing.py", line 69, in app
    await response(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/responses.py", line 174, in __call__
    await self.background()
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/background.py", line 43, in __call__
    await task()
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/background.py", line 26, in __call__
    await self.func(*self.args, **self.kwargs)
  File "/Users/bhavaniravi/invisible/playground/fastapi_exceptions/app.py", line 37, in background_task
    raise PlaygroundError("custom error", 3000)
exception.PlaygroundError: ('custom error', 3000)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/uvicorn/protocols/http/h11_impl.py", line 429, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
    return await self.app(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/fastapi/applications.py", line 276, in __call__
    await super().__call__(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/applications.py", line 122, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/errors.py", line 184, in __call__
    raise exc
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/errors.py", line 162, in __call__
    await self.app(scope, receive, _send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/exceptions.py", line 83, in __call__
    raise RuntimeError(msg) from exc
RuntimeError: Caught handled exception, but response already started
```

Let's deconstruct this error a bit.

1. The error is caused by `starlette/middleware/exceptions.py` and the `ExceptionMiddleware` class
2. The message `print ("playground exception handled")` was never printed in the stack trace, showing the handler wasn't called
3. `The above exception was the direct cause of the following exception:` and `Caught handled exception, but response already started` in stack trace shows that RuntimeError is a direct cause of mishandling the exception.

We need a better way that

1. Calls the exception handler for background task
2. But, does not print the crazy stack trace

Let's try different alternatives of exception handler hook to work around this error.

### Version 1 - Capturing RuntimeError

Instead of handling global exceptions, how about we handle the `RuntimeError`?

```python
async def handle_exception(request, exc):
    if isinstance(exc, RuntimeError):
        print("handling runtime exception", exc)     
```

Having just the runtime error handler won't handle `PlaygroundError` since it is the cause of `RuntimeError`

```python
app.add_exception_handler(RuntimeError, handle_exception)
```

Having both `PlaygroundError` and `RuntimeError` still, result in `RuntimeError` since it's the result of the `ExceptionMiddleware` unable to gracefully handle the `PlaygroundError`

```python
app.add_exception_handler(PlaygroundError, handle_exception)
app.add_exception_handler(RuntimeError, handle_exception)
```

### Version 2 - Capturing Global Exception

`RuntimeError` is a type of `Exception` so why not add a global exception handler and handle specific cases inside the handler function?

~~app.add\_exception\_handler(ACEException, handle\_exception)~~

```python
async def handle_exception(request, exc):
    if isinstance(exc, RuntimeError) and isinstance(exc.__cause__, ACEException):
        print("handling runtime exception", exc)
    if isinstance(exc, PlaygroundError):
        print("handling custom exception", exc)
    else:
        print("handling other exception", exc)
    return JSONResponse({"detail": str(exc)})

app.add_exception_handler(Exception, handle_exception)
```

Two things's different about this version

1. This version doesn't throw a runtime error
2. The handler is called and `handling custom exception` message is printed

**What's the catch?**

There is still the exception log that looks like this, making it hard to understand whether the exception was handled cleanly

```bash
handling custom exception ('custom error', 3000)
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/uvicorn/protocols/http/h11_impl.py", line 429, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
    return await self.app(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/fastapi/applications.py", line 276, in __call__
    await super().__call__(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/applications.py", line 122, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/errors.py", line 184, in __call__
    raise exc
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/errors.py", line 162, in __call__
    await self.app(scope, receive, _send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
    raise exc
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
    await self.app(scope, receive, sender)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
    raise e
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/routing.py", line 718, in __call__
    await route.handle(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/routing.py", line 69, in app
    await response(scope, receive, send)
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/responses.py", line 174, in __call__
    await self.background()
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/background.py", line 43, in __call__
    await task()
  File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/background.py", line 26, in __call__
    await self.func(*self.args, **self.kwargs)
  File "/Users/bhavaniravi/invisible/playground/fastapi_exceptions/app.py", line 37, in background_task
    raise PlaygroundError("custom error", 3000)
exception.PlaygroundError: ('custom error', 3000)
```

#### Maybe it's just an error log

Maybe it is. But...

1. How can you differentiate?
2. When debugging an error after 6 months, how can you know if this is a result of a handled or unhandled exception
3. This will create logs that might trigger alerts from Datadog or Sentry.



Before considering alternative approaches, we have to ensure that we aren't doing anything wrong and there is no other way possible. For that, we need answers to the following two questions.

#### Why is this happening?

Going through the error logs deeper will bring out a few things.

The following line from `RuntimeError` Version 1

```bash
 File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/errors.py", line 184, in __call__
    raise exc
```

The following line from `PlaygroundErorr` Version 2

```bash
File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/starlette/middleware/errors.py", line 184, in __call__
    raise exc
```

It says one thing clearly... **Starlette is the culprit**

The error is being raised by `Starlette` not `FastAPI`. To verify that, I created a Starlette app and boom. It was the culprit.

Try running the following Starlette app. It also raises the same error.

```python
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from middleware import CustomMiddleware
from starlette.middleware import Middleware
from exception import PlaygroundError


def error_handler(request, exc):
    print("error handled gracefully")


def raise_exception():
    raise PlaygroundError("Something went wrong")


async def endpoint(request):
    return Response("Hello, world!", background=BackgroundTask(raise_exception))


app = Starlette(
    routes=[Route("/", endpoint=endpoint)],
    exception_handlers={Exception: error_handler},
    middleware=[Middleware(CustomMiddleware, debug=True)],
)

```

#### Where is the error log coming from?

[This line in uvicorn](https://github.com/encode/uvicorn/blob/e2a39792cc65e45d9ccc5a3908fc79aaa75b7b12/uvicorn/protocols/http/h11\_impl.py#L412) is where it is coming from. Though it's not raising the exception, it is still alarming to have the log.

#### What can we do about it?

We can find the first point of contact  `FastAPI` and figure out a way to hook exception-handling Behavior, and BOOM!

```bash
File "/Users/bhavaniravi/.virtualenvs/python-everyday/lib/python3.9/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
    raise e
```

There we have it. It's a middleware that's raising the exception. How about we write one to suppress the exception we need?

### Version 3 - Let's Write a Middleware

Let's write a custom middleware in Starlette style and capture the playground error.

```python
# custom_middleware.py

class CustomExceptionHandlingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope, receive)
            try:
                await self.app(scope, receive, send)
            except PlaygroundError as err:
                logging.exception("Error occured while making request to ACE")
                return handle_exception(request, err)
        else:
            await self.app(scope, receive, send)
            return None
```

Link the middleware to the app

```python
# app.py

app.add_middleware(CustomExceptionHandlingMiddleware)
```

Hitting the background API after adding the middleware `localhost:8000/background` captures the error gracefully without spitting those huge logs.

### Does it work for all cases?

#### Case 1 - Synchronous API with Exceptions

With just the middleware and not the `exception_handler` Synchronous APIs go haywire.

Create an endpoint that throws the error

```python
@app.get("/")
def index():
    raise PlaygroundError("custom error", 3000)
```

Removing all exception handlers and just keeping the middleware will result in the following error

```
ERROR:    ASGI callable returned without starting response.
INFO:     127.0.0.1:59350 - "GET / HTTP/1.1" 500 Internal Server Error
```

**Solution**

Clup them both, use `exception_handlers` and `CustomMiddleware`

**Why does this happen?**

> Yet to find an answer

#### Case 2 - Error in both sync API and background task

If the API has an error in both sync and background, according to the FastAPI the background tasks won't be executed, hence we are good.

```python
@app.get("/")
def index(bg: BackgroundTasks):
    bg.add_task(background_task)
    raise PlaygroundError("custom error", 3000)
    return {"message": "Hello World"}
```

#### Case 3 - TestCases

At this point, I was happy with my solution. Everything was working smoothly and then came the test cases.

Even with the `CustomExceptionHandlingMiddleware` I couldn't get rid of `RuntimeError: Caught handled exception, but response already started.` the error. That is because the `TestClient` we use with FastAPI has `raise_server_exceptions` set to `True` by default.

We can, of course, set it to `False` but in the main project, we'd be constraining fellow developers to write code a certain way. We need a better way

**Additional Handler?**

How about adding extra logic to our custom middleware?

```python
try:
    ...
except PlaygroundError:
    ...
except RuntimeError as err:
    if isinstance(err.__cause__, PlaygroundError):
        print("Error occured while making request to ACE")
        return handle_exception(request, err.__cause__)
raise
```

This helps us handle the `RuntimeErorr` Gracefully that occurs as a result of unhandled custom exception

\---

There is a Middleware to handle errors on background tasks and an exception-handling hook for synchronous APIs. However, this feels hacky and took a lot of time to figure out. FastAPI developers deserve better both in terms of documentation and errors.



### **Other Things I Considered But Didn't Do**

### **Custom Background Task**

&#x20;In FastAPI all background task functions are wrapped around `BackgroundTask` class. We can extend that to handle a custom error. But that'd be constraining developer behavior for future development

### FastAPI Style Middleware

If you dig through FastAPI documentation enough you will find it recommending `app.add_middleware` as a decorator or extending `BaseHTTPMiddleware`

Something like this

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        content_type = request.headers.get('Content-Type')
        print(content_type)
        
        # process the request and get the response    
        response = await call_next(request)
        
        return response
```

This doesn't work because the exceptions we are dealing with happen at the Starlette middleware stack level. Doesn't matter how much I tried this particular case, the dispatch method was never reached. Maybe if I dig more I can find the why?