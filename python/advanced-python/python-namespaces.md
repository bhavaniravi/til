---
description: How Python figures out the scope of it's variables?
---

# Python Namespaces & Variable Scope

> Namespaces are one honking great idea—let’s do more of those!
>
> — [_The Zen of Python_](https://www.python.org/dev/peps/pep-0020)_, by Tim Peters_

The Namespace is one of the most beautiful concepts in Python. [Bound vs Unbound](bound-vs-unbound-functions-in-python.md) variable sheds a little light on how variables are accessed and their scope. But let's dive deeper and see how it happens exactly

Think of the namespaces of a dictionary in a Python program. Namespaces are created at different moments and have different lifetimes. Every time you create an object(variables, functions), an associated namespace gets updated so that the next time you refer to the same variable, you can get its value.

Open Python shell and type the following

```python
globals()
```

What do you see?

{% code overflow="wrap" lineNumbers="true" %}
```python
# I understand some of you are away from your system

{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>}
```
{% endcode %}

There are different kinds of namespaces. Let's look at each of them in detail.

### Built-in Namespace

In Python, we don't have to import certain functions or objects, they seem to be available to us in handy. But how?

```python
sum([10, 20])
max(10, 20)
```

The namespace containing the built-in names, such as sum, max, etc., is created when the Python interpreter starts up (before even globals) and is never deleted. The built-in names actually also live in a python module; this is called **builtins**

All the built-in objects are loaded into the program via `__builtins__` namespace

```python
dir(__builtins__) # will print a huge list
```

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption><p>Global namespace vs Builtins illustration</p></figcaption></figure>

### Global Namespace

The global namespace for a module is created when the module definition is read in; normally, module namespaces also last until the interpreter quits.&#x20;

The statements executed by the top-level invocation of the interpreter, either read from a script file or interactively, are considered part of a module called **main**, so they have their own global namespace

```python
print ("Globals 1:", globals())

x = 10
y = 26
d = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6}

def get_val(key):
    return d.get(key)

print ("Globals 2:", globals())
```

**Output**

{% code overflow="wrap" %}
```python
Globals 2: {'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x100b852e0>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'trial.py', '__cached__': None, 'x': 10, 'y': 26, 'd': {1: 2, 2: 3, 3: 4, 4: 5, 5: 6}, 'get_val': <function get_val at 0x100c09550>}
```
{% endcode %}

Think of globals as a **universal dictionary for the module.** Every time you create an object(including function) or import a module at the module level(ie., outside all functions), the global namespace gets updated. On deleting the objects, the same gets removed from the namespace

### Local Namespace

The local namespace for a function is created when the function is created and deleted when the function returns or raises an exception that is not handled within the function. (Actually, forgetting would be a better way to describe what actually happens.)&#x20;

Each recursive invocation of a function will have its own local namespace.

In fact, all operations that introduce new names use the local scope: in particular, import statements and function definitions bind the module or function name in the local scope.

Let's take a look at the following snippet of code. There are three things to notice

1. There are two variables with the same name `name`
2. They are printed at two different places - Inside & outside the function
3. The function is called to see what it prints&#x20;

<pre class="language-python"><code class="lang-python">name = "global name"

def new_function():
    name = "local name"
    print (name)

new_function()
<strong>print (name)</strong></code></pre>

#### Output&#x20;

```python
local name
global name
```

As expected, the global variable's value was not affected by the local variable despite it being the same variable name. That is because

1. &#x20;The local namespace is different from the global namespace
2. The Python interpreter looks for variables in the nearest local namespace before escalating the search to the global namespace

<figure><img src="../../.gitbook/assets/image (2) (3).png" alt=""><figcaption><p>Local namespace</p></figcaption></figure>

#### Locals Method

Similar to `globals()` you can use `locals()` to get all the local objects pertaining to that scope

```python
def new_function():
    a = 10
    b = 20
    name = "local name"
    print (locals()) # {'a': 10, 'b': 20, 'name': 'local name'}
new_function()
```

_At global scope \`globals()\` and \`locals()\` value is the same. Voila_

```python
print (locals() == globals()) #  prints true
```

### Referring Global Variables&#x20;

Now, what if there was a case where you had to tell the function scope to use the variable defined in the `global` scope? Worry not! We have a `global` variable.&#x20;

```python
pythoname = "global name"
print (name)

def new_function():
    global name
    name = "local name"
    print (name)
    print (locals())

new_function()
print (name)
```

In the above snippet, the global keyword is used to refer to the global `name`,  thereby updating it to a new value.&#x20;

#### Output&#x20;

```
global name
local name
{}
local name
```

_Also_, _notice that the \`locals()\` dict remains untouched since there are no variables defined in the local scope._

### Enclosing-Namespace

Python is known for its nested functions. _Oh! those decorators! Yet another fascinating topic. More on that later._ Let's take the following function as an example

We have a variable `new_1` defined in 3 different scopes Inner function, outer function, and global, and is printed at each level

```python
new_1 = "global_1"

def outer_function():
    new_1 = "outer_1"

    def inner_function():
        new_1 = "inner_1"
        print ("inner_function new_1=", new_1)
    
    inner_function()
    print ("outer_function new_1=", new_1)
    

outer_function()
print ("global new_1=", new_1)
```

**Output**

```
inner_function new_1= inner_1
outer_function new_1= outer_1
global new_1= global_1
```

The magic begins when you start to comment out `new_1` variable from the innermost scope to the outer.

Comment `new_1 = "inner_1"` and the output becomes

```
outer_function new_1= outer_1
inner_function new_1= outer_1
global new_1= global_1
```

Comment `new_1 = "outer_1"` and the output becomes

```
outer_function new_1= global_1
inner_function new_1= global_1
global new_1= global_1
```

_We went through all this trouble to understand that the variable resolves itself to the nearest enclosing scope. In our case, \``outer_function`\`._

### nonlocal keyword

Similar to `global` keyword `nonlocal` is used to refer to variables at the enclosing namespace

```python
    def inner_function():
        nonlocal new_1
        new_1 = "inner_1"
        print ("inner_function new_1=", new_1)
```

Modifying the value of nonlocal variables changes the variable in the enclosing namespace.

**Output**

```
inner_function new_1= inner_1
outer_function new_1= inner_1
global new_1= global_1
```

### Global vs. Non-local

Using `global` keyword instead of `nonlocal` will directly refer to the global variable discarding all other enclosing scopes

```python
    def inner_function():
        global new_1
        new_1 = "inner_1"
        print ("inner_function new_1=", new_1)
```

**Output**

```
inner_function new_1= inner_1
outer_function new_1= outer_1
global new_1= inner_1
```

### Scope of a Variable&#x20;

We have been referring `scope` throughout this post. It's high time that we provide a formal definition of it

> A **scope** is a textual region of a Python program where a namespace is directly accessible. “Directly accessible” here means that an unqualified reference to a name attempts to find the name in the namespace.

When a variable is referred in the code, the Python interpreter searches for it in the following order

1. Local scope
2. Enclosing scope
3. Global scope
4. Built-in scope

### **Exercise For You**

_Import a module, let's say \`import math\` in different scopes global, enclosing, and local. Find out what \`globals()\` and \`locals()\` method outputs in each case_
