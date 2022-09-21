---
title: What Happens During Docker Build and Run?
sub_title: Disecting How Docker works, One layer at a time
slug: what-happens-during-docker-build-and-run
tags:
  - devops
featuredImgPath: https://i.imgur.com/P6LyCHX.png
isexternal: true
published_date: 2021-12-14T00:00:00.000Z
created_date: 2021-12-14T00:00:00.000Z
draft: false
description: >-
  When using Docker, you will encounter two major operations `build` and `run`.
  The build command creates a docker image based on the `Dockerfile`. The run
  command uses the created docker image to run a
---

# What Happens During Docker Build and Run?

When using Docker, you will encounter two major operations `build` and `run`. The build command creates a docker image based on the `Dockerfile`. The run command uses the created docker image to run a container.

But, what do these mean? What's an image? What does running a container mean?

To understand this question further, let's create a Docker image.

```
FROM ubuntu:18.04
RUN apt-get update && apt-get install -y python3 python3-dev python3-pip nginx

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app/app.py" ]
```

When building the image it starts with a base image followed by running each command in layers.

## Docker Building Images

Dive a tool to dissect docker images into its layers gives us a sneak peek of what goes on when we `docker build <image-path:tag>`

1. Docker starts by spinning up the container of the base image and runs the next command on the file
2. Captures the files changed during this process along with metadata
3. The changed files called as changedset is stored in `layer.tar` and the associated metadata in layer.json

[Jamie Duncan has dissected a Docker image in detail to understand the metadata and changeset better](https://medium.com/@jamieeduncan/dissecting-a-docker-container-image-6da2411fcebe)

## Docker Running Containers

Tying it all together, Though there were container technologies before the Docker era, Docker made the process easy, maintainable, and reproducible.

When running a docker container by default

1. Creates a PID namespace to run all the processes inside the container
2. Allocates a default of 6m memory. A container can scale to use as much CPU as it needs.
3. Creates a thin Read-write layer on top of the image layers. This layer will hold all the data from writes inside the container.

Along with the above items, there is a tonne of other parameters that you can tweak when running a Docker container. [Docker documentation has more info about it.](https://docs.docker.com/engine/reference/run/)

The namespace, allocated resources, and the R/W layer are all deleted when the container is removed.
