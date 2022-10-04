---
description: How Python figures out the scope of it's variables?
---

# Unbound Variables in Python

Consider the following example&#x20;

```python
def take_sum(a, b, c):
    return a+b+c

def main():
    print(take_sum)

main()
```

Outputs&#x20;

```
<function take_sum at 0x1031c84c0>
```

Python looks for `take_sum` in local scope ie., inside main followed by global scope whereas,

```python
def main():
    if "take_sum" not in globals():
        take_sum = lambda x,y,z: x+y+z
    print(take_sum)
```

Returns: `UnboundLocalError: local variable 'take_sum' referenced before assignment`

The function raises an exception because the compiler saw that the code _could_ assign to `take_sum` as a local variable, and so it makes all the references to `take_sum` in the code be local. You can no longer look up the global variable `take_sum` in the normal way once that determination has been made.

To understand how variable names are resolved read [Python Namespaces](broken-reference)
