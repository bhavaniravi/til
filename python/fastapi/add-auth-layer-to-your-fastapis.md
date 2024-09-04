---
added: Jan 05 2024
draft: false
image: null
unusedLayout: ../layouts/BlogPost.astro
slug: add-auth-layer-to-your-fastapis
sub_title: Protect your FastAPI API with authentication, compliation of methods that
  will and won't work
tags:
- fastapi
title: Add Auth Layer to Your FastAPIs
---

# Add Auth Layer to Your FastAPIs

Our whole backend now runs on FastAPI. It would be undermining to say I'd fallen in love with it, but a better word is, _"Dear FastAPI, you've dearly replaced Flask."_

Contrary to The Zen of Python(There should be one-- and preferably only one-- obvious way to do it), we often encounter libraries that don't necessarily follow this rule or at least make us think twice before choosing one way or another.

The same happens when you add an Auth layer for your FastAPI and APIs.

***

When it was time to implement an auth layer, we had several options.

* Write a middleware
* Write a custom Router
* Use ApiAuth Header

Looking back, the answer should've been relatively straightforward, only that it was not.

To give you some context, FastAPI was new for my team and me. Over the last 8 months, we have become comfortable with certain features over others. One such thing was middleware.

The team decided that was easier since we already had [a few working middlewares](https://www.bhavaniravi.com/python/fastapi/the-pain-of-building-a-centralized-error-handler-in-fastapi).

### Auth Layer with FastAPI middleware

Here is a simplified version of FastAPI middleware that reads the `Authorization` header and fetches the user. If it fails to do either, it will return a 401.

```python
class AuthMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http" or scope.get("path") in [
            "/docs",
        ]:
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", []))
        authorization_header = headers.get("Authorization")
        if authorization_header:
            request.state.user = await fetch_user(
                authorization_header,
            )
            await self.app(scope, receive, send)
            return

        response = Response("Unauthorized", status_code=401)
        await response(scope, receive, send)

from fastapi import APIRouter, FastAPI

app = FastAPI()
app.add_middleware(AuthMiddleware)

@app.get(
    "/",
    summary="Get Health Status",
)
def get_health_status():
    return "Ok"
```

There are a few things to note here.

1. The 1st version of this code was complicated, resulting in [Runtime Stream Error](https://github.com/getsentry/sentry-python/issues/1675) when coupled with sentry.
2. We haven't extended our middleware from a pre-defined class; that's a pattern we found most FastAPI middleware follow.
3. When we deployed it, the OpenAPI docs could not set the auth header.

The 3rd point was more concerning for us, given we are a team of 8+ developers constantly developing, testing, and deploying APIs, and our docs are the first point of contact for new APIs

![](https://substackcdn.com/image/fetch/w\_1456,c\_limit,f\_auto,q\_auto:good,fl\_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f1a7913-6a58-4b4c-b29e-760bc78f34c0\_1464x996.png)

### FastAPI Depends

The familiar concept for us was `Depends.` adding a dependency on the router level. Infact, FastAPI recommends it.

> For many scenarios, you can handle security (authorization, authentication, etc.) with dependencies, using `Depends()`

```python
from fastapi import Depends, Security

def auth_header(Authentication: str = Header()):
    if auth != CONST_AUTH_KEY:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

router = APIRouter(
    prefix="/v1",
    tags=["API v1"],
    dependencies=[Depends(auth_header)],
)

@router.get(
    "/health",
    summary="Get Health Status",
)
def get_health_status():
    return "Ok"

app.include_router(router)
```

That would seem to work like a charm... until... you hit the API

Despite passing the Authorization header from the UI, you can see the field is missing an error.&#x20;

![](https://substackcdn.com/image/fetch/w\_1456,c\_limit,f\_auto,q\_auto:good,fl\_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb955bb70-c1d6-43cf-aed6-63eb5e153dc2\_1464x996.png)

If you inspect the network call, you can see that the specified header will be dropped from

![](https://substackcdn.com/image/fetch/w\_1456,c\_limit,f\_auto,q\_auto:good,fl\_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe1fdd0c-4543-4ec3-9a96-e43680107dee\_1024x344.png)

### FastAPI Security

Unfortunately, FastAPI security also has a similar effect with `Header` for the same reason that auth headers are dropped from the request

```python
from fastapi import Security

...

router = APIRouter(
    prefix="/v1",
    tags=["API v1"],
    dependencies=[Security(auth_header)],
)

```

What a bummer! Technically, both these methods should work. Unfortunately, it doesn't. Don't worry. We haven't run out of options yet.

_**We have a couple more, and both works.**_

### FastAPI HttpBearer

Unlike our previous method, where `auth_header` a mere `Header`. In this method, we will be passing an `HTTPBearer` object wrapped in `Security` an object to `auth_header` dependency does the trick.

```python
from fastapi.security import HTTPBearer

CONST_AUTH_KEY='temp-key'

def auth_header(Authentication: str = Security(HTTPBearer())):
    if Authentication != CONST_AUTH_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )

router = APIRouter(
    prefix="/v1",
    tags=["API v1"],
    dependencies=[Depends(auth_header)],
)
```

### FastAPI APIKeyHeader

In this method, we will be splitting the authentication logs into two parts

1. Check whether the right key format is passed on the request `Header`&#x20;
2. Use the Auth Middleware from method 1 to ensure that the right key is passed

```python
from fastapi.security import APIKeyHeader

auth_header = APIKeyHeader(name="Authorization", auto_error=True)

router = APIRouter(
    prefix="/v1",
    tags=["API v1"],
    dependencies=[Security(auth_header)],
)

app.add_middleware(AuthMiddleware)
```