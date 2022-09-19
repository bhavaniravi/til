# Multi-Processing Vs Multi-Threading

### Multi-Threading

* Threads share the same memory space
* GIL ensures two threads do not update the same memory
* Great for I/O bound tasks such as making a HTTP call, reading a file or DB
* Threads are concurrent ie., two or more threads appear to run at the same time
* Threads are easier to spin
* Communication between threads are easier since it shares the memory space

### Multi-Processing

* Each process has it's own memory space
* Great for CPU bound tasks such as sorting an array, fibonacci series, grayscaling an image
* Takes advantage of multiple CPU cores
* Processes are parallel. ie., two or more processes will actually run at the same time
* Processes take a little longer to spin than threads due to the memory overhead
* Communication between processes involes writing to a location and reading from it

### Example

```python
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import urllib.request as ur

datas = []


def get_from(url):
    connection = ur.urlopen(url)
    data = connection.read()
    datas.append(data)


urls = [
    "https://python.org",
    "https://docs.python.org/",
    "https://wikipedia.org",
]


def timeit(func):
    def wrapper(*args, **kwargs):
        import time

        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start} seconds")
        return result

    return wrapper


@timeit
def thread():
    with ThreadPoolExecutor() as ex:
        for url in urls:
            ex.submit(get_from, url)


@timeit
def multi():
    with ProcessPoolExecutor() as p:
        for url in urls:
            p.submit(get_from, url)


if __name__ == "__main__":
    thread()
    multi()
    # print(datas)

```

