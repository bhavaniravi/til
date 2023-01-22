# Types of Databases & When to Use them

Databases are _**knowledge**_ _**gods**_ of our application (Fun term right? Yeah I think so too). And just like gods Databases are many, we have so many options to choose from.&#x20;

When you're a backend developer you cannot dodge this question in interviews. The understanding not just helps you in the interview but also signals that you're a developer who knows the right tool for right job

### In-Memory DB

- Used mainly for caching
- Data is stored as key value pairs
- The values are stored in-memory and are volatile
- common examples are redis, memcache, etcd(used by kubernetes)

### Relational

- It works like a charm for well structured data with relations
- Supports ACID properties Works well for applications that needs atomic transactions
- Horizontal scaling is not supported but most cloud platforms are trying to work around them&#x20;
- Famous examples are MySQL & Postgres
- Well suited for transactional workloads OLTP

### NoSQL

#### DocumentDB

- Works well for unstructured data
- Faster reads means increased perfomance
- Examples are Mongodb, Cassandra
- DB can be horizontally and vertically scaled

#### ColumnDB

- Did I hear analytics, use ColumnDB
- Because analytics involves comparing two features X and Y and you would be comparing a data in a particular colum
- They are typically less efficient for inserting new data (Why?)
- Well suited for OLAP

### Graph

- Works well for Data that's structured in the form of graphs
- Unlike relational DB the data is defined in the form of node and edges(it's relationshops)
- Best usecase is for social media application like FB, twitter
- Example: Neo4j

### TimeSeries DBs

- Timeseries database stores data against a time and other metadata
- Best example is monitoring applications&#x20;
- Data is stored in a hypertable and chunked into columns of metadata & time agaisnt the actual data
- This Talk clearly explains it [https://www.youtube.com/watch?v=eQKbbCg0NqE](https://www.youtube.com/watch?v=eQKbbCg0NqE)
- InfluxDB, TimeseriesDB, Prometheus

### Datawarehouse

### MultiModel DB

---

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
