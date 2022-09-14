# Data Model in Python

> First you learn to program, then you learn the programming language. \
> And yes, those are two different things

Every Python newbie get's their mind blown when they come across this concept. It can be alarming but also exciting. Let me start with a snippet of code to explain you what we are about to explore. Before you proceed any further just ensure you have understanding classes & objects

Spend sometime going through the code below. What are the things you notice?

{% code title="custom.py" %}
```python
class Number:
    def __init__(self, num):
        self.num = num
    
    def __add__(self, obj):
        return self.num + obj.num
    
a = Number(10)
b = Number(20)

print (a + b)
```
{% endcode %}

Here are a few thoughts you might have got

**Why not just do this?**

```python
a = 10
b = 20
 
print (a + b)
```

Two reasons

1. We are in advanced python section
2. I'm setting the stage to teach something but you're up to something in finding the above snippet relatable

Let me break some news to you, look at the following snippet. Does that look familiar to you?&#x20;

```python
a = int(10)
b = int(20)
 
print (a + b)
```

> Big realization 1: int is a class&#x20;

**What does `__add__` do?**

That's a great question. If you have ran this snippet on your system. Try adding a few print statements and comment out addition statement

```python
def __add__(self, obj):
    print (self)
    print (obj)
    return self.num + obj.num

# print (a + b)
```

> Big realization 2: `__add__` method takes two objects as attributes and returns the sum of num attribute in both the objects

**Does that mean..... int also has an `__add__` method?**

```
>>> dir(int)

['__abs__', '__add__', '__and__', '__bool__', '__ceil__', '__class__', 
'__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', 
'__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', 
'__getnewargs__', '__gt__', '__hash__', '__index__', '__init__', 
'__init_subclass__', '__int__', '__invert__', '__le__', '__lshift__', 
'__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', 
'__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', 
'__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', 
'__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', 
'__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', 
'__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', 
'__trunc__', '__xor__', 'as_integer_ratio', 'bit_length', 'conjugate', 
'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes']
```

**Does other arithmetic operations work the same way?**

Yes, so does comparision operators, so does every other data type.

### **Everything is an object**

In python. every piece of data is an object of a class. It has a value and an identity that uniquely identifies the object

```python
a = int(10)
print (id(10))
```

### Type of Class Determines Type of Operations

The kind of operators I can use on an object is defined by it's class type.

For example,&#x20;

len() cannot be performed on integers

### Objects Can be mutable or Immutable

Objects whose values can be updated are called **mutable object,** if not they're **immutable objects**

```python
# mutable
a = 10
a = a + 20

# immutable
l = (1, 2, 3)
l = l + (1, 2, 3)

# note, line 10, 11 doesn't mean it's mutable
# it's just object is reinitialized
l = (1, 2, 3)
l = (3, 2, 1)
```

### Memory Representation: Reference Counting

Objects are references to the values stored in the memory not the value itself. To understand this better

```
a = "avc"
b = "avc"

c = "ab"

print (id(a), id(b))
print (id(cNNN))
```

Can you see both the ids are same? It's a memory optimization that Python performs, it keeps the frequently used integer values in memory to quickly create the object.

But that's not the awestrucking part, when learning C/C++ we are asked to visualize memory representation differently as compared to what happens with Python

> _**Reference counting is the number of objects refering to the same memory location at any given time**_

In this case the reference count of value "avc" is 2

![Memory representation of Python object](<../../.gitbook/assets/image (2) (1).png>)

Now let's update the value of b and see what happens `b = "ram`"

![Memory representation when the object is updated](<../../.gitbook/assets/image (3).png>)

You can see that the reference to old value is removed and a new reference is maintained

### Object Deletetion&#x20;

Things get interesting when objects are deleted. Let's say we are deleting b with `del b` statement. The value remains in the memory while the reference to the object is removed.

![](<../../.gitbook/assets/image (1).png>)

**Garbage collector** goes through them and removes all the values in the memory for which the reference count is 0

