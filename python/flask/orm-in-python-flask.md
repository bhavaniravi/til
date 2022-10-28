---
description: ORM in flask a quick start tutorial
---

# ORM in Python Flask

### What is ORM?

ORM(Object Relationship Mapping) is a programming construct where the DB tables are treated as objects, and the operations on top of them are carried out via functions.

### Video Tutorial

{% embed url="https://www.youtube.com/watch?v=xpqW8o1jEdg" %}

### ORM in Python

Django, the web framework in Python, has one of the most solid ORMs. For non-Django applications, SQLAlchemy has proved to be effective.

### ORM in Flask

Flask doesn't support ORM out of the box, but with the help of `flask-sqlalchemy`, we can achieve the ORM functionalities.

### Installation

```
pip install flask-sqlalchemy
```

### Documentation For Reference

Flask SQLalchemy has extensive documentation.

https://flask-sqlalchemy.palletsprojects.com/en/2.x/

### Configure DB

Let's start writing some code. Open a Python file `orm_example.py.`

Import flask-sqlalchemy and connect to the DB

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
```

### Defining a Model

Each table is called a Model(a Python class) when defining an ORM. The table columns will become attributes of the class.

```
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    joined_on = = db.Column(db.DateTime, nullable=False)
```

### Creating the Table

The above snippet is just a configuration to create a table in DB. You need to use

```
db.create_all()
```

### CRUD Operations

#### Create a new Item

```
# creates a Python Object
admin = User(username='admin', email='admin@example.com')

# adds to the db session
db.session.add(admin)

# Makes the entry in the DB
# you can do multiple db.session.add before committing
db.session.commit()
```

#### List all items

```
users = User.query.all()

results = [] 
for user in users:
    results.append({
        "username": user.name,
        "email": user.email
    })
```

#### Filter Items

```
users = User.query.filter_by(username='admin').all()
# use the same for loop as above
```

#### GET by id

```
user = User.query.filter_by(id=1).first()
result = {
    "name": user.name,
    "email": user.email
}
```

#### Selecting Specific Columns

```
fields = ["book_id", "book_name", "author"]
field_objects = [getattr(Book, "name") for field in fields]
books = Book.query.with_entities(*field_objects).all()
```

#### Update an Item

```
User.query.filter_by(id=1).update({"name": "admin001"})
db.session.commit()
```

#### Delete an Item

```
user = User.query.filter_by(id=1).first()
db.session.delete(user)
```

### Run the script

```
python orm_example.py
```

### How to add One-Many and Many-Many relationship

Checkout the following snippet

https://github.com/bhavaniravi/work-tracker/blob/main/application/models.py

### Exercise

1. Pick one model for your application
2. Add the Model and fields
3. Try all the CRUD operations
