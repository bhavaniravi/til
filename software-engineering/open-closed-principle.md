---
added: Aug 13 2022
draft: false
image: null
layout: ../layouts/BlogPost.astro
slug: open-closed-principle
sub_title: Open for extension closed for modification
tags:
- software-engineering
title: Open-Closed Principle
---

# Open-Closed Principle

Open closed principle is one of the SOLID principle appeared in 1988 book [_Object Oriented Software Construction_](https://en.wikipedia.org/wiki/Object-Oriented_Software_Construction).

Open-closed principle states that software entities such as classes modules and functions should be open for extension and should be closed for modification

- _A module will be said to be open if it is still available for extension. For example, it should be possible to add fields to the data structures it contains, or new elements to the set of functions it performs._
- _A module will be said to be closed if \[it] is available for use by other modules. This assumes that the module has been given a well-defined, stable description (the interface in the sense of information hiding)._

### Example

Consider the following class that exports data in different formats

```
class Export:
    def export_pdf(self):
        print ("export to pdf")

    def export_json(self):
        print ("export to json")
```

Later you want to introduce a new data format let's say XML, your first intiution is to go and modify the export class and add a new function. Open-close principle is against this.

We need to design our classes in such a way that future changes are extension rather than modification

```
class Export:
    def export(self):
        NotImplementedError()

class ExportPdf(Export)
    def export(self):
        print ("export to pdf")

class ExportJson(Export)
    def export(self):
        print ("export to json")
```

### Isn't it just composition?

That's what I thought to. From the looks of it we are inducing the behavior into the class but just using composition doesn't comply to OC principle

Infact you can comply to OC principle with both Inheritance and composition

### But.. But??

Don't be alarmed when you see a code that doesn't comply to OC principle. No your colleague is not stupid. Things to remember

- Initial abstractions will never be able to accommodate all future requirement changes.
- Principles are guidelines. They aren't strict rules
- Premature optimization can introduce uncessary complexity. If you extend the export class when you have just pdf then we are introducing unnecessary complexity

### References

- [https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)
