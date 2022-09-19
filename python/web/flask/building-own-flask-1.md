---
title: Building OwnFlask - A Flask(like) Python Framework
sub_title: Reverse Engineering Flask app to build a similar flask like interface
slug: building-own-flask-1
tags: ["python/web/flask"]
featuredImgPath: https://i.imgur.com/Zq4lJgB.jpg
isexternal: true
published_date: 2021-09-16
created_date: 2021-09-16
description: In order to demistify `flask` these I had two options either to
  read Flask code end to end and understand or reverse engineer flask by
  building one on my own. I chose the latter and this blog is a step by step log
  of how it went.
draft: false
---
# Writing Your Own Flask(like) Framework

I have been wanting to demystify what goes behind the Python Flask framework. How does defining something as simple as `app.route` handle HTTP Requests? How does `app.run` creates a server and maintains it?

To demystify `flask` these, I had two options 
Read Flask code end to end and understand or
Reverse engineer flask by building one on my own. 
I chose the latter, and this blog is a step-by-step log of how it went.

**Side Note**

If you are new to Flask, then [How to build your 1st flask app](https://medium.com/bhavaniravi/build-your-1st-python-web-app-with-flask-b039d11f101c) might be a good place to start.

## Reverse Engineering

A simple Flask application looks something like this.

```
# demo.py
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    return "hello"

if __name__ == "__main__":
    app.run()
```

Reverse engineering started in my head. I am going to be working with just two files, `ownflask.py` and `demo.py`.

Here is how a simple flask application would look



Looking at this sample snippet, I want to mimic the same interface. Take a pass from top to bottom and see what all we need

1. We need a class `Flask` which initializes an `app` object
2. The `Flask` class has a method `run`, and it starts a server
3. The `Flask` class also has a `route` method that registers the endpoints

Let's lay them down

```
#ownflask.py


class Flask:
    def __init__(self, name):
        self.name = name
    
    def run(self):
        pass
        
    def route(self, path, methods):
        def wrapper(f):
            pass
        return wrapper

```

That's gives us the basic skeleton. Let's add the functionality one by own. Python [http](https://docs.python.org/3/library/http.server.html) module provides an `HTTPServer` let's use that.

## Starting a Server

In Flask, `app.run` is responsible for starting a development webserver. The server then listens to all HTTP requests and responds to them.

```
#ownflask.py

from http.server import HTTPServer, BaseHTTPRequestHandler

class Flask:
    ...
    
    def run(self, server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=8000):
        server_address = ('', port)
        print (f"Running server in port {port}")
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

```

In `demo.py`, change `from flask` to `from ownflask` to work with the module we just created and run `demo.py`. On hitting the `http://127.0.0.1:8000` from the browser, you get a 501 error since we haven't implemented anything to handle the incoming request.


![Error response on running ownflask](https://i.imgur.com/HryJiE1.png) 


### Mapping Requests

The `app.route` method in Flask registers an endpoint. When an HTTP request comes, it maps it to the associated function call. These routes are maintained in a global object so that the request handler can refer to it. For our `ownflask`, let's use a global dictionary.

Here I have two methods one to record the `routes` to its associated functions and `route_methods` to associate endpoints and its HTTPMethods.
 
```
routes = {}
route_methods = {}

class Flask:
    ...
    def route(self, path, methods):
        def wrapper(f):
            routes[path] = f
            route_methods[path] = methods
        return wrapper
```

### Handling GET Request

When running our server, we have used a `BaseHTTPRequestHandler`. From the Python documentation, it is clear that we have to extend it to support handling requests.


> By itself, it cannot respond to any actual HTTP requests; it must be subclassed to handle each request method (e.g., GET or POST).


```

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str.encode("Handling GET"))
    
    def do_POST(self):
        pass
```

The above snippet sends `Handling GET` as a response despite what the route function returns. Let's change that.

`dir(self)` returns that `self.path` is the URL, mapping that with routes dict, we can call the respective function.


```
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        resp = routes[self.path]()
        ...
        ...
        self.wfile.write(str.encode(resp))
```

### Handling URL Params

Flask is known for passing URL params as a part of a URL string or a query string.

```
/book/<int:id>
/book?id=10
```

The 1st one would require some form of regex in the routes and the way we store them. Let's handle them later. Let's handle `hello world` with the name `http://127.0.0.1:8000?name=Joe`

The current code fails with a `KeyError` since the query string is also a part of the route. 

```
KeyError: '/?name=jpe'
```

To parse this and separate the URL path and the query params, we will use `urllib`

```
import urllib.parse as urlparse


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlparse.urlparse(self.path).path
        qs = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        resp = routes[path]()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str.encode(resp))
```

In Flask, the routing function can access the request params via the global `Request` object. In our case, for the `hello` route to access query params, we need the means to pass it to them. 


### Request Class 


```
class Request:
    def __init__(self, request, method):
        self.request = request
        self.method = method
        self.path = urlparse.urlparse(request.path).path
        self.qs = urlparse.parse_qs(urlparse.urlparse(request.path).query)
        self.headers = request.headers
```

Let's pass this Request object to the route.

```
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        request = Request(self, "GET")
        resp = routes[request.path](request)
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str.encode(resp))
```

With the current state, `hello() takes 0 positional arguments but 1 was given` let's capture `request`

```
@app.route("/")
def hello(request):
    return f"hello {request.qs["name"][0]}"
```

### Handling JSON Response

If we modify the `hello` endpoint to return a `dict` instead of `str`, we will receive an error.

> descriptor 'encode' for 'str' objects doesn't apply to a 'dict' object

It happens because we convert dict to a bytes object. To do this, we should convert the response dict to `str` and then encode it.

```
def do_GET(self):
    request = Request(self, "GET")
    resp = routes[request.path](request)
    if isinstance(resp, dict):
        resp = json.dumps(resp)
```



### Handling POST Request

For handling POST requests, you need to access the request body along with other parameters. Let's update the request class to support the same.

```
class Request:
    def __init__(self, request, method):
        ...
        ...
        self.content_length = int(self.headers.get('content-length', 0))
        self.body = request.rfile.read(self.content_length)
        try:
            self.json = json.loads(self.body)
        except json.decoder.JSONDecodeError: 
            self.json = {}
```

Let's consume the same via a POST API


```
@app.route("/todo", methods=["POST"])
def todo(request):
    return {"status": "success", "data": request.json}
```

### Handling Unsupported Request

Right now, if you hit `/todo` from the browser, you will get the response. This is wrong since we have clearly defined that `/todo` on supports post request. This is where `route_methods` comes in really handy.

```
def do_GET(self):
    ...
    if "GET" not in route_methods[request.path]:
        self.send_response(401)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str.encode(f"{request.path} {request.method} not supported"))
        return
```

Looks like we are repeating ourselves a lot; let's move them to a common function


```
class RequestHandler(SimpleHTTPRequestHandler):
    ...
    ...
    def write_response(self, response, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if isinstance(response, dict):
            response = json.dumps(response)
        self.wfile.write(str.encode(response))
```

The final `do_GET` and `do_POST` method looks like this.

```
    def do_GET(self):
        request = Request(self, "GET")
        if "GET" not in route_methods[request.path]:
            self.write_response("Method not supported", 401)
            return
        resp = routes[request.path](request)
        self.write_response(resp, 200)
    
    def do_POST(self):
        request = Request(self, "POST")
        if "POST" not in route_methods[request.path]:
            self.write_response("Method not supported", 401)
            return
        resp = routes[request.path](request)
        self.write_response(resp, 200)
```

We can further refactor them into 

```
    def not_found(self, request):
        return self.write_response(f"{request.path} 404 NOT FOUND", 404)

    def method_not_supported(self, request):
        return self.write_response(f"{request.path} {request.method} not supported", 401)
        
    def process_request(self, request):
        if request.path not in routes:
            return self.not_found(request)
        if request.method in route_methods[request.path]:
            return self.method_not_supported(request)
        
        resp = routes[request.path](request)
        self.write_response(resp)
    
            
    def do_GET(self):
        request = Request(self, method='GET')
        return self.process_request(request)

    def do_POST(self):
        request = Request(self, method='POST')
        return self.process_request(request)

```

### Introducing Multi-Threading

At this point, if you write a small multithreading script and hit our server, it will hang because `HTTPServer` is not designed to handle multiple requests. Replacing it with `ThreadingHTTPServer.` 

```
from http.server import ThreadingHTTPServer

class Flask:
    ...
    def run(self, name):
        ...
        ...
        self.server = WSGIServer((self.host, self.port), ThreadingHTTPServer)

```


### WSGI vs HTTP

At this point, I was happy with what I accomplished and already posted a [tweet](https://twitter.com/BhavaniRavi_/status/1428294719138799618?s=20) and [ArunMozhi](https://arunmozhi.in/) nudged me in the direction to explore `WSGIServer`.



```
from wsgiref.simple_server import WSGIServer

class Flask:
    ...
    def run(self, name):
        ...
        ...
        self.server = WSGIServer((self.host, self.port), HttpReqHandler)

```

---
What started as an experiment to Demyistify flask and understand it better got me into a rabbit hole of new questions. 

1. How is `WSGIServer` different from `HTTPServer` the interface looks the same?
2. How can we plug the `ownflask` to work with Gunicorn
3. How to add async to ownflask?
4. Going one step further, How does Gunicorn work?
5. What are my unknown unknowns?

If you know the answer to any of these, you can send them to me via [Twitter](https://twitter.com/BhavaniRavi_)

