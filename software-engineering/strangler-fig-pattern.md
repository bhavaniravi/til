# Strangler Fig Pattern

I came across this pattern in a Reddit thread where the [person asked how to stay on top of modern ](https://www.reddit.com/r/ExperiencedDevs/comments/w71nh2/how\_to\_keep\_up\_modern\_dev\_skills/)technologies, and it straight-up pointed to this [Freecodecamp article](https://www.freecodecamp.org/news/what-is-the-strangler-pattern-in-software-development/amp/)

> Strangler fig pattern aims to incrementally update large legacy codebases without strangling the functionality of the system
>
> It's derived from how stranglers affect growth of a fig tree

For example, when you want to change the legacy API with a new one, instead of rewriting the old code, you can write a new interface and route the traffic to the new one.

Repeating this pattern will result in updating legacy systems with limited risk and better productivity

### Further Reading

* [7 Programming Anti-Patterns](https://thelearning.dev/7-programming-anti-patterns)



{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
