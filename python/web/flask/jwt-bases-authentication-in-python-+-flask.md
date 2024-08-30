---
added: Aug 15 2022
description: null
layout: ../layouts/BlogPost.astro
slug: jwt-bases-authentication-in-python-+-flask
tags:
- flask
title: JWT Bases Authentication In Python + Flask
---

# JWT Bases Authentication In Python + Flask

I have compiled the theory of all [Authentication methods in the blog](https://bhavaniravi.com/blog/authentication-in-python/)

#### Why JWT?

* Works for mobile based, web based and microservices based auth
* Relatively easy to implement
* Commonly used in industry

#### Implementation

**Install Flask-Jwt Library**

```
pip install Flask-JWT
```

**Initiallize JWT object**

JWT needs a private key to decode the JWT token. Here it's `super-secret`. In production systems we usually have this key in a seperate file. If a secret key of an application is exposed anyone can start using the APIs generating API tokens

```
# File :: app.py

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3000)
```

**Create a User Model in `models.py`**

```
# File :: models.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))
```

**Write an authenticate function.**

Flask-JWT uses two functions for auth purposes

**1. Authenticate**

Logs in the user for the first time and returns the user object. Internally, JWT uses this object to create JWT token.

**2. Identity**

Identity function is used on all protected APIs. Internally flask-jwt decodes JWT token and gets the user\_id and passes it to `identity` is function.

```
File :: api.py

from flask_jwt import jwt_required, JWT, current_identity

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user
        
jwt = JWT(app, authenticate, identity)
```

**Write Signup and Authenticated views**

```
# File :: api.py

@app.route("/signup", methods=["POST"])
def signup():
    params = request.json()
    try:
        user = User(**params)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return {"Status": "Error", "result": "User already exists"}, 400
    return {"Status": "Success", "result": "User created"}
```

Inorder to autheticate your APIs you need to add the decorator `jwt_required` to the view function

```
@app.route("/work")
@jwt_required()
def list_work_items():
    result = WorkItem.query.filter_by(created_by=current_identity.id).all()
    response = [{"id": res.id, "title":res.title} for res in result]
    return {"Status": "Success", "result": response}
    
```

**`/auth` API uses the above function to authenticate a user, returns JWT token**

`/auth` is an API that comes as default in the flask-jwt package. To login a user make an API call with username and password

```
params = {
    "username": "joe",
    "password": "pass"
}

requests.post("/auth", json=params)
```

**The future requests can use JWT Token for authentication**

```
headers = {
    "Authorization" : "JWT <token>"
}
requests.get("/workitems", headers=headers)
```