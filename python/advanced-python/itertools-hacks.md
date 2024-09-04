---
added: Aug 15 2022
description: null
unusedLayout: ../layouts/BlogPost.astro
slug: itertools-hacks
tags:
- advanced-python
title: Itertools Hacks
---

# Itertools Hacks

### Avoiding nested loops

Without Itertools

```
for elem1 in list1: 	
    for elem2 in list2: 		
        process(elem1, elem2) 
```

With Itertools

```
import itertools 
for elem1, elem2 in itertools.product(list1, list2): 	
    process(elem1, elem2) 
```

And of course the itertools example, if it is as simple as a single function call, can be shortened to :

```
map(process, itertools.product(list1, list2) ) 
```

Also it can be extended to multiple lists, iterables etc, without needing to have another nested loop.

### Infinite loop with a count

Without Itertools

```python
iteration = 0 
while True: 	
    process( iteration ) 	
    iteration +=1 
```

With Itertools

```python
import itertools 
for iteration in itertools.count(): 	
    process( iteration) 
```

no risk of ever stepping past the increment line by doing a continue for instance (been there, done that)

***

### Running lists together

Without Itertools

```python
for element in list1 + list2 + list3: 	
    process( element ) 
```

With Itertools

```
import itertools 
for element in itertools.chain( list1, list2, list3): 	
    process(element) 
```

**Itertools with list of list**

```
import itertools 
for element in itertools.chain.from_iterable( list_of_lists ): 	
    process(element) 
```

### List with Condition

Without Itertools

```
for element in my_list:    
    if condition(element): 		
        break    
    process(element) 
```

With Itertools

```
import itertools 
for element in itertools.takewhile(lambda x: not condition(x), my_list): 	
    process(element) 
```