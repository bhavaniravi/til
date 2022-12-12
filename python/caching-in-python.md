---
slug: caching-in-python
published_date: 2019-08-26T00:00:00.000Z
created_date: 2019-08-26T00:00:00.000Z
title: Caching in Python
template: post
draft: false
subtitle: A blog to help you understand caches in detail
tags:
  - python
featuredImgPath: /media/caching-in-python.png
description: >-
  Caching, is a concept that was gifted to software world from the hardware
  world, A temporary storage for fast and easy access of data.
---

# Caching in Python

Caching, is a concept that was gifted to software world from the hardware world. A cache is a temporary storage area that stores the used items for easy access. To put it in layman’s terms, it is the chair we all have.

This blog covers the basics of

1. [What are Caches?](caching-in-python.md#Conventional-Caches)
2. [Caching Operations](caching-in-python.md#Caching-Operations)
3. [Cache Eviction Policies](caching-in-python.md#Cache-Eviction-Policies)
4. [Implementation of Cache Eviction Policies](caching-in-python.md#LRU-Implementation)
5. [Distributed Caching](caching-in-python.md#Distributed-Caching)
6. [Caching In Python](caching-in-python.md#Caching-In-Python)

## Conventional Caches

In the world of computer science, Caches are the hardware components that store the result of computation for easy and fast access. The major factor that contributes to the speed is its memory size and its location. The memory size of the cache is way less than an RAM. This reduces the number of scans to retrieve data. Caches are located closer to the consumer (CPU) hence the less latency.

## Caching Operations

There are two broad types of caches operation. Cache such as Browser caches, server caches, Proxy Caches, Hardware caches works under the principle of `read` and `write` caches.

When dealing with caches we always have a huge chunk of memory which is time consuming to read and write to, DB, hard disk, etc., Cache is a piece of software/hardware sitting on top of it making the job faster.

### Read Cache

A read cache is a storage that stores the accessed items. Every time the client requests data from storage, the request hits the cache associated with the storage.

1. If the requested data is available on the cache, then it is a **cache hit**.
2. if not it is a **Cache miss**.
3. Now when accessing a data from cache some other process changes the data at this point you need to reload the cache with the newly changed data this it is a **Cache invalidation**

### Write Cache

Write caches as the name suggests enables fast writes. Imagine a write-heavy system and we all know that writing to a DB is costly. Caches come handy and handle the DB write load which is later updated to the DB in batches. It is important to notice that, the data between the DB and the cache should always be synchronized. There are 3 ways one can implement a write cache.

1. Write Through
2. Write Back
3. Write Around

#### Write Through

The write to the DB happens through the cache. Every time a new data is written in the cache it gets updated in the DB.

**Advantages** - There won’t be a mismatch of data between the cache and the storage

**Disadvantage** - Both the cache and the storage needs to be updated creating an overhead instead of increasing the performance

#### Write Back

Write back is when the cache asynchronously updates the values to the DB at set intervals.

This method swaps the advantage and disadvantage of _Write through_. Though writing to a cache is faster of **Data loss and inconsistency**

#### Write Around

Write the data directly to the storage and load the cache only when the data is read.

* **Advantages**
  * A cache is not overloaded with data that is not read immediately after a write
  * Reduces the latency of the write-through method
* **Disadvantages**
  * Reading recently written data will cause a cache miss and is not suitable for such use-cases.

## Cache Eviction Policies

Caches make the reads and write fast. Then it would only make sense to read and write all data to and from caches instead of using DBs. But, remember the speed comes only because caches are small. Larger the cache, longer it will take to search through it.

So it is important that we optimize with space. Once a cache is full, We can make space for new data only by removing the ones are already in the cache. Again, it cannot be a guessing game, we need to maximize the utilization to optimize the output.

The algorithms used to arrive at a decision of which data needs to be discarded from a cache is a **cache eviction policy**

1. LRU - Least Recently Used
2. LFU - Least Frequently Used
3. MRU - Most Recently Used
4. FIFO - First In First Out

#### LRU - Least Recently Used

As the name suggest when a cache runs out of space remove the `least recently used` element. It is simple and easy to implement and sounds fair but for caching `frequency of usage` has more weight than when it was last accessed which brings us to the next algorithm.

#### LFU - Least Frequently Used

LFU takes both the age and frequency of data into account. But the problem here is frequently used data stagnates in the cache for a long time

#### MRU - Most Recently Used

Why on earth will someone use an MRU algorithm after talking about the frequency of usage? Won’t we always re-read the data we just read? Not necessarily. Imaging the image gallery app, the images of an album gets cached and loaded when you swipe right. What about going back to the previous photo? Yes, the probability of that happening is less.

#### FIFO - First In First Out

When caches start working like queues, you will have an FIFO cache. This fits well for cases involving pipelines of data sequentially read and processed.

## LRU Implementation

Caches are basically a hash table. Every data that goes inside it is hashed and stored making it accessible at O(1).

Now how do we kick out the least recently used item, we by far only have a hash function and it’s data. We need to store the order of access in some fashion.

One thing we can do is have an array where we enter the element as and when it is accessed. But calculating frequency in this approach becomes an overkill. We can’t go for another Hash table it is not an access problem.

A doubly linked list might fit the purpose. Add an item to the linked list every time it is accessed and maintain it’s a reference in a hash table enabling us to access it at O(1).

When the element is already present, remove it from its current position and add it to the end of the linked list.

## Where to Place the Caches?

The closer the caches are to its consumer faster it is. Which might implicitly mean to place caches along with the webserver in case of a web application. But there are a couple of problems

1. When a server goes down, we lose all the data associated with the server’s cache
2. When there is a need to increase the size of the cache it would invade the memory allocated for the server.

The most viable solution is to maintain a cache outside the server. Though it incorporates additional latency, it is worth for the reliability of caches.

**Distributed Caching** is the concept of hosting a cache outside the server and scaling it independently.

## When to Implement Caches?

Finding the technologies to implement caches is the easiest of all steps. Caches promises high speed APIs and it might feel stupid not to incorporate them, but if you do it for wrong reasons, it just adds additional overhead to the system. So before implementing caches make sure

1. The hit to your data store is high
2. You have done everything you can to improve the speed at DB level.
3. You have learnt and researched on various caching methodologies and systems and found what fits your purpose.

## Implementation In Python

To understand caching we need to understand the data we are dealing with. For this example I am using a simple MongoDB Schema of `User` and `Event` collections.

We will have APIs to get `User` and `Event` by their associated IDs. The following code snippet comprise a helper function to get a respective document from MongoDB

```
def read_document(db, collection, _id):
    collection = db[collection]
    return collection.find_one({"_id": _id})
```

### Python inbuilt LRU-Caching

```
from flask import jsonify
from functools import lru_cache

@app.route(“/user/<uid>“)
@lru_cache()
def get_user(uid):

    try:
        return jsonify(read_user(db, uid))
    except KeyError as e:
        return jsonify({”Status": “Error”, “message”: str(e)})
```

LRU-Caching like you see in the following example is easy to implement since it has out of the box Python support. But there are some disadvantages

1. It is simple that it can’t be extended for advanced functionalities
2. Supports only one type of caching algorithm
3. LRU-Caching is a classic example of server side caching, hence there is a possibility of memory overload in server.
4. Cache timeout is not implicit, invalidate it manually

### Caching In Python Flask

To support other caches like redis or memcache, Flask-Cache provides out of the box support.

```
config = {’CACHE_TYPE’: ‘redis’} # or memcache
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

@app.route(“/user/<uid>“)
@cache.cached(timeout=30)
def get_user(uid):
    try:
        return jsonify(read_user(db, uid))
    except KeyError as e:
        return jsonify({”Status": “Error”, “message”: str(e)})
```

With that, We have covered what caches are, when to use one and how to implement it in Python Flask.

## Resources

1. [You’re Probably Wrong About Caching](https://msol.io/blog/tech/youre-probably-wrong-about-caching/)
2. [Caching - Full Stack Python](https://www.fullstackpython.com/caching.html)
3. [Redis Vs Memcache](https://medium.com/@Alibaba\_Cloud/redis-vs-memcached-in-memory-data-storage-systems-3395279b0941)
4. [Caching - A Trip Down the Rabbit Hole](https://www.youtube.com/watch?v=bIWnQ3F1eLA)
5. [All About Caching](https://www.mnot.net/blog/caching/)
