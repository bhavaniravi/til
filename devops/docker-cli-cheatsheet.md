# Docker CLI Cheatsheet

### How to get exit code of a docker container?

```
docker inspect c2c769c4b9ef --format='{{.State.ExitCode}}'
```

### Docker-Compose strconv.Atoi: parsing "": invalid syntax

```
docker-compose down --remove-orphans`
```

### Docker container keeps running despite entry point being a script in Compose?

Check if restart is set to always

```
restarts: "no" #don't miss the quote
```

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
