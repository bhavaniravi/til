---
description: A deeper understanding from Python Docs
---

# Python Namespaces

_The following section of the blog will quote lines from actual Python Docs and try to explain them in simple English with examples_

> A namespace is a mapping from names to objects. Most namespaces are currently implemented as Python dictionaries, but that’s normally not noticeable in any way (except for performance), and it may change in the future.

When you create a variable `x=10` you are adding x to namespace. It's more of a labeling an object rather than allocating a memory box and stamping it

```
x = 10
print (globals())
```

Examples of namespaces are: the set of built-in names (containing functions such as abs(), and built-in exception names); the global names in a module; and the local names in a function invocation. In a sense the set of attributes of an object also form a namespace.

```
__builtins__
gloabal()
local
NonLocal
classObject.__dict__
```

The important thing to know about namespaces is that there is absolutely no relation between names in different namespaces; for instance, two different modules may both define a function maximize without confusion — users of the modules must prefix it with the module name.

```
start = 0

def range():
    start = 0
    
class Help:
    start = 0
    
# All these starts are in different namespace
```

> Attributes may be read-only or writable. In the latter case, assignment to attributes is possible. Module attributes are writable: you can write modname.the\_answer = 42. Writable attributes may also be deleted with the del statement. For example, del modname.the\_answer will remove the attribute the\_answer from the object named by modname.

Let's create two modules `mod1.py` and `mod2.py`

```
# mod1.py
this_answer = 39
```

```
# mod2.py

import mod1
mod1.this_answer = 32
del mod1.this_answer
```

Namespaces are created at different moments and have different lifetimes.

* The namespace containing the built-in names is created when the Python interpreter starts up, and is never deleted.
* The global namespace for a module is created when the module definition is read in; normally, module namespaces also last until the interpreter quits. The statements executed by the top-level invocation of the interpreter, either read from a script file or interactively, are considered part of a module called **main**, so they have their own global namespace. (The built-in names actually also live in a module; this is called builtins.)
* The local namespace for a function is created when the function is called, and deleted when the function returns or raises an exception that is not handled within the function. (Actually, forgetting would be a better way to describe what actually happens.) Of course, recursive invocations each have their own local namespace.

> A **scope** is a textual region of a Python program where a namespace is directly accessible. “Directly accessible” here means that an unqualified reference to a name attempts to find the name in the namespace.

Although scopes are determined statically, they are used dynamically. At any time during execution, there are 3 or 4 nested scopes whose namespaces are directly accessible:

* the innermost scope, which is searched first, contains the local names
* the scopes of any enclosing functions, which are searched starting with the nearest enclosing scope, contains non-local, but also non-global names
* the next-to-last scope contains the current module’s global names
* the outermost scope (searched last) is the namespace containing built-in names

If a name is declared global, then all references and assignments go directly to the middle scope containing the module’s global names.

> To rebind variables found outside of the innermost scope, the **nonlocal** statement can be used; if not declared nonlocal, those variables are read-only (an attempt to write to such a variable will simply create a new local variable in the innermost scope, leaving the identically named outer variable unchanged).

Usually, the local scope references the local names of the (textually) current function.

> Outside functions, the local scope references the same namespace as the global scope: the module’s namespace.

> Class definitions place yet another namespace in the local scope.

It is important to realize that scopes are determined textually: the global scope of a function defined in a module is that module’s namespace, no matter from where or by what alias the function is called. On the other hand, the actual search for names is done dynamically, at run time — however, the language definition is evolving towards static name resolution, at “compile” time, so don’t rely on dynamic name resolution! (In fact, local variables are already determined statically.)

A special quirk of Python is that – if no global or nonlocal statement is in effect – assignments to names always go into the innermost scope.

> Assignments do not copy data — they just bind names to objects. The same is true for deletions: the statement del x removes the binding of x from the namespace referenced by the local scope.

In fact, all operations that introduce new names use the local scope: in particular, import statements and function definitions bind the module or function name in the local scope.

The global statement can be used to indicate that particular variables live in the global scope and should be rebound there; the nonlocal statement indicates that particular variables live in an enclosing scope and should be rebound there.
