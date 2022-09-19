# GIL

GIL stands for global interpreter lock. [Python Data Model ](data-model-in-python.md)post talks about how data is stored and referenced internally in Python. GIL ensures referenced variables are not deleted or modified by multiple threads simultaeoulsy.

> In CPython, the **global interpreter lock**, or **GIL**, is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once. The GIL prevents race conditions and ensures thread safety. &#x20;

* Everytime a new thread is spun the thread aquires the GIL ie., it owns the objects in the memory space.&#x20;
* No other threads can modify or delete until the GIL is released
* The thread with access to the GIL runs it's job and hands the control back to main thread
* This is considered as a disadvantage but Python provides coroutines and multiprocessing to work around this
