---
title: Pydantic Tips, Tricks and Comparison with Dataclasses and Attrs
sub_title: Pydantic cool features and what makes it better than Dataclasses and Attrs
slug: pydantic-tips-tricks
tags:
  - python
featuredImgPath: 
isexternal: true
published_date: "2023-07-02"
created_date: "2023-06-30"
draft: false
description: >-
  Pydantic is a Python library for data validation and settings management using Python type hinting. In this post, we will look at some of the tips and tricks of Pydantic and compare it with Dataclasses and Attrs
---

# Pydantic - Tips, Tricks and Comparison with Dataclasses and Attrs

Recently, I got introduced to Pydantic. I was heavily using FastAPI and absolutely love how it enforces you to use Pydantic for Data serialization and validation. Life before Pydantic was mostly flask and Django. While both of these were great frameworks, we need something like FastAPI to even see where it is flawed. Enough about FastAPI, this post is not about that. Let's go back to Pydantic

> The blog post is published on 2nd July 2023, but will keep on updated as I learn more Pydantic tricks

## What is Pydantic?

It is a Python library. You do `pip install pydantic` and come into some powerful stuff. It is a library for data validation and settings management using Python type hinting. It is primarily used to validate data coming into your application and serialize data going out of your application. It is a superset of Python's dataclasses and attrs library.

A simple pydantic model looks like this

```python
from pydantic import BaseModel
import datetime

class Publisher(BaseModel):
    name: str
    location: str
    started_date: datetime.date

class BookModel:
    name: str
    publisher: Publisher
    price: float
    isbn: str
    published_date: datetime.date
```

For the rest of this post we will use the above snippet as our example and make changes to it and explore Pydantic features.

### Data Serialization

1. Data serialization from Dict

```python
book_dict = {
    "name": "The Alchemist",
    "publisher": {
        "name": "HarperCollins",
        "location": "New York"
    },
    "price": 10.0,
    "isbn": "978-0062315007",
    "published_date": "2014-05-01"
}

book = BookModel(**book_dict)
```

2. Data serialization from JSON

```python
import json
book_json = json.dumps(book_dict)
book = BookModel.parse_raw(book_json)
```

Pretty cool right? Now let's see what happens when you poke around with wrong data format

### Data Validation

1. Marking fields as optional

```python
from typing import Optional

class BookModel:
    ...
    published_date: Optional[datetime.date]
```

2. Make year greater than 1800

```python
from pydantic import Field

class BookModel:
    ...
    published_date: datetime.date | None = Field(None, gt=datetime.date(1800, 1, 1))
```

3. Validate ISBN

To add a custom validation to a field, you can use the `validator` decorator

```python
from pydantic import validator


class BookModel:
    ...
    @validator("isbn")
    def isbn_must_be_valid(cls, v):
        regex = "^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$"
        if not re.search(regex, v):
            raise ValueError("Invalid ISBN")
```

4. Validate all fields

There will be cases where you want to validate one field based on another field. You can use the `root_validator` decorator to validate all fields

```python
from pydantic import root_validator, BaseModel

class Book(BaseModel):
    ...

    @root_validator
    def check_published_date(cls, values):
        if values.get("published_date") < values.get("publisher").get("started_date"):
            raise ValueError("Book cannot be published before publisher started")

```

5. So how does it work?

```python
book = BookModel(name= "The Alchemist",
                publisher=Publisher(name="HarperCollins",
                                    location="New York"),
                price=10.0,
                isbn="abcdef", # error
                published_date="1799-05-01" # error
)
```

### Configure Models

1. Configuring fields

```python
from pydantic import Field

class BookModel:
    name: str = Field(..., min_length=3, max_length=50, alias="book_name")
    publisher: Publisher
    price: float = Field(..., gt=0)
    isbn: str = Field(..., regex="^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$")
    published_date: datetime.date = Field(..., gt=datetime.date(1800, 1, 1))
```

2. Configuring model

We can add `Config` class to configure the model to tweak the behavior of the model. For example, we can set `extra` to `forbid` to prevent extra fields from being added to the model. We can also set `allow_population_by_field_name` to `True` to allow population of model by field name. We can also set `fields` to a dictionary of field name and its configuration. For example, we can set `alias` for a field.

```python
from pydantic import BaseModel, Field

class BookModel(BaseModel):
    ...

    class Config:
        extra = "forbid"
        allow_population_by_field_name = True
        fields = {
            "name": {
                "alias": "book_name"
            },
            "published_date": {
                "alias": "published"
            }
        }
```

3. Setting common alias

```python
from pydantic import BaseModel, Field

def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))

class BookModel(BaseModel):
    ...
    class Config:
        extra = "forbid"
        allow_population_by_field_name = True
        alias_generator = to_camel

```

There are a lot more config which you can explore in the [docs](https://docs.pydantic.dev/latest/usage/model_config/)

### Inheritance whoooho!

Inheritance with pydantic becomes even more powerful since we are also inherting the config from the parent class.

```python
class EbookModel(BookModel):
    format: str

class AudioBookModel(BookModel):
    duration: int

class PaperBookModel(BookModel):
    weight: float
```

### DeSerializing Data

1. Serialize to Dict

```python

book_model.dict() # all fields
book_model.dict(exclude={"isbn"}) # exclude isbn
book_model.dict(exclude={"isbn"}, by_alias=True) # use alias
book_model.dict(include={"name", "price", "publisher": {"name"}}) # only these fields
book_model.dict(exclude_unset=True) # removes all None
```

2. Serialize to JSON

```python
book_model.json() # all fields
book_model.json(exclude={"isbn"}) # exclude isbn
```

3. Pickle

```python
import pickle

book_model_bytes = pickle.dumps(book_model)
```

## Pydantic Settings

Pydantic settings are a way to configure the behavior of the model. We can configure the settings in 3 ways

1. Config class
2. Decorator
3. Context manager

## Comparison with other libraries

### Dataclasses

Let's start by writing a sample dataclass

```python
from dataclasses import dataclass
import datetime

@dataclass
class Publisher:
    name: str
    location: str

@dataclass
class Book:
    name: str
    price: float
    isbn: str
    published_date: datetime.date
```

Now let's see how we can use this dataclass to validate data

```python
book = Book(name= "The Alchemist",
            publisher=Publisher(name="HarperCollins",
                                location="New York"),
            price="abcd",
            isbn="abcdef",
            published_date="1799-05-01"
)
```

Gives an error `TypeError: __init__() got an unexpected keyword argument 'publisher'`. Let's fix that and retry.

```python
book = Book(name= "The Alchemist",
            price="abcd",
            isbn="abcdef",
            published_date="1799-05-01"
)
```

That passed. But notice how we didn't get any error for the `price` field. That's because dataclasses don't validate data.

Let's see how we can add validation to dataclasses

```python

from dataclasses import dataclass, field, fields
from typing import Optional
import datetime

@dataclass
class Book:
    ...

    def __post_init__(self):
        for field in fields(self):
            if field.name == "price":
                if not isinstance(field.value, float):
                    raise ValueError("Price must be a float")
            elif field.name == "isbn":
                regex = "^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$"
                if not re.search(regex, field.value):
                    raise ValueError("Invalid ISBN")
            elif field.name == "published_date":
                if field.value < datetime.date(1800, 1, 1):
                    raise ValueError("Published date must be greater than 1800")
```

That's a lot of hoops to jump through. The code doesn't look clean. We cannot blame Dataclass completely for this. Dataclasses were not designed to validate data. They were designed to create classes with less boilerplate. To keep it generic we had to compensate on lack of powerful features like pydantic.

## Want validation? but with dataclass?

Pydantic got you covered in that aspect `from pydantic.dataclasses import dataclass` and you can use it just like you would use dataclass.

### Attrs

Attrs is another library which is similar to dataclasses. Attrs is more closer to pydantic than dataclasses. Let's see how we can use attrs to validate data. They have pretty good argument on why you should use attrs over dataclasses. You can read it [here](https://www.attrs.org/en/stable/why.html)

```python

from attrs import asdict, define, make_class, Factory

@define
class Publisher:
    name: str
    location: str

@define
class Book:
    name: str
    price: float
    isbn: str
    published_date: datetime.date
    publisher: Publisher = Factory(Publisher, name="HarperCollins", location="New York")

    # book cannot be created without a publisher
    __attrs_post_init__ = lambda self: self.publisher
    # published date should be >= 1800
    published_date_validator = validator("published_date")(lambda self, attribute, value: value >= datetime.date(1800, 1, 1))


book = Book(name= "The Alchemist",
            price="abcd",
            isbn="abcdef",
            published_date="1799-05-01"
)
```
