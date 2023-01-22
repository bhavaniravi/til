# Apache Airflow + MongoDB

### Run Mongo Docker Container

```jsx
docker run -p 27018:27017 \\
-e MONGO_INITDB_ROOT_USERNAME=admin \\
-e MONGO_INITDB_ROOT_PASSWORD=password -d mongo \\
```

### Test Mongo Connection

```jsx
import pymongo
# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb://admin:password@0.0.0.0:27018/admin?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception as e:
    print(e, "Unable to connect to the server.")
```

### Setting up airflow connection

Under Airflow connection create a new Airflow connection with host, password and username

### Mongo Hook

```jsx
from airflow.providers.mongo.hooks.mongo import MongoHook

hook = MongoHook(mongo_conn_id='mongo')
client = hook.get_conn()

try:
    print(client.server_info())
except Exception as e:
    print(e, "Unable to connect to the server.")
```

Adding sample data to mongo

```jsx
docker exec -it <container-id> -- /bin/bash
mongo -u admin
use notes
db.createCollection("notes")
db.notes.insertMany(
   [
     { "note": "Create an identity", "_id":1 , "archived": false},
     { "note": "0.1% increment every day", "_id":2, "archived": true},
     { "note": "productivity is quality not quantity","_id":3, "archived": true}
   ]
)
```

### Setting up s3 localstack

```jsx
docker run --rm -it -p 4566:4566 localstack/localstack -e SERVICES=s3
```

Create a s3 bucket

```jsx
aws --endpoint-url=http://localhost:4566 s3 mb s3://notes
```

---

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
