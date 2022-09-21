---
title: Introduction to Docker - The What, Why and How
sub_title: images, containers, commands what does all these mean in Docker
slug: docker-introduction
tags:
  - devops
featuredImgPath: https://i.imgur.com/nokXidS.jpg
isexternal: true
published_date: 2021-11-29T00:00:00.000Z
created_date: 2021-11-29T00:00:00.000Z
draft: false
description: >-
  Docker let's you packages application and it's associated packages and
  libraries to be ran anywhere without much hassle.
---

# Introduction to Docker - The What, Why and How

## The Art of Shipping Software

The core of Docker and its success is in its ability to solve the long-standing problem of Shipping Software. As we saw in the introductory video, deploying software involved a lot of "It works on my machine" There was no concrete way to ship software and its associated packages and libraries until then.

So repeat after me

> Docker lets you packages application and their associated packages and libraries that can run anywhere without hassle.

## Images

Docker image is a file. It contains a set of instructions to construct Docker containers and run them. Docker images solve the shipping part of the software. All you have to do is build a docker image file, and it can run in any Dockerized environment.

## Containers

Containers are actual running instances of an image. Each docker container runs the program built into the image in its isolated environment which enables us to run multiple Docker containers into the same machine

## Dockerfile

Every time you think of Dockerizing an application create a Dockerfile. In the Dockerfile, we will use the basic docker commands to build and deploy the application. You can think of Dockerfile as a Lego block instruction manual properly laid out that lets us build the end structure without much hassle.

## Registry

The Docker Registry is a centralized repository to store and retrieve built Docker images. You can think of registries as a Github for Docker images. Registries can be public like Dockerhub or private like the one that your company runs.

## Docker Commands

If you're using Docker you will often use these commands maps to common Docker functions.

1. Create an image - `docker build`
2. Pull an image from registry - `docker pull`
3. Push an image - `docker push`
4. Run a container - `docker run <image-id>`
5. Stop a container - `docker stop <container-id>`

## Dockerizing an Application

Let's say you have a Python Flask application that looks like this

```
python-docker
|____ app.py
|____ requirements.txt
|____ Dockerfile
```

To Dockerize it, we start with Dockerfile and a base image.

> A base image is a pre-built docker image that contains a basic set of libraries that can be extended to build other images.

```
# start with a base image
FROM python:3.8-slim-buster

# change the current dir in Docker
WORKDIR /app

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all contents of the directory
COPY . .

# Run the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```
