---
added: Sep 19 2022
created_date: 2021-12-12 00:00:00+00:00
description: Docker is one of the most powerful tools to ship and deliver software.
  While celebrating that, we shouldn't forget the predecessor inventions that went
  in at the OS level that made Docker possible
draft: false
featuredImgPath: https://i.imgur.com/AzQqzQB.png
image: null
isexternal: true
layout: ../layouts/BlogPost.astro
published_date: 2021-12-12 00:00:00+00:00
slug: docker-virtualization-vs-containerization
sub_title: 'Evolution of docker '
tags:
- devops
title: Docker - Virtualization vs Containerization
---

# Docker - Virtualization vs Containerization

When the internet became a thing, we started hosting things on bare metal servers. In the last five years, we have moved from there to this fancy thing called Docker that changed our lives.

So far, we have discussed various [aspects of the DevOps system](https://youtu.be/m31asTwC_s8) and [Docker's what, why, and how](../blog/docker-introduction/). To delve deeper into Docker's internals, we need to understand a few operating system terms.

Oh no! It sounds boring! I thought so too, but actually, it's not. But to make our lives easier, we are only going to learn two things.

**System Processes** - The system runs and controls in its secluded way. E.g., boot loader, device drivers.

**User Processes** - The processes you can run and control as a user. E.g., Running a Python script.

## Virtualization - The Starting Point

Initially, we had a single-threaded operating system, which could handle only one task at a time, which fitted the single-core systems perfectly.

Then we had multi-core CPUs leading to multi-threaded operating systems enabling us to run different programs simultaneously.

Taking this up a notch, IBM came up with the brilliant idea of running multiple OS while sharing the hardware across these operating systems leading to Virtualization.

## Types of Virtualization

### Hardware Level Virtualization

Hardware virtualization is the isolation of hardware resources to run multiple OS.

**Full virtualization** is when the hardware system is emulated. The Guest OS does not know whether it deals with actual or simulated hardware. The hypervisor is the piece of software that does the job of emulation so perfectly.

**Paravirtualization** is when certain parts of the OS are modified to work with a special API interface. The OS will know that it isn't talking to the actual hardware but emulated software.

There are, of course, pros and cons for each method, but for the sake of simplicity, the takeaway here should be Multiple OS sharing hardware resources.

### OS Level Virtualization

The era of containers begin. Instead of running multiple OS on top of a single hardware, OS Level Virtualization focuses on providing isolated userspace for programs to run user processes (refer to the first two definitions) without affecting each other.

These isolated user spaces are called Containers and form the foundation of today's Docker. Unlike virtual machines, containers have the same base OS, i.e., process-level isolation and not OS Level.

## Containerization

OS-level virtualization is the base for containers, thereby Dockers. Unlike hardware emulation to OS, we need to give user processes that it owns everything(Emulation). Thankfully you don't need a new fancy piece of software like a hypervisor. The Linux kernel itself got us covered.

### Cgroup

Cgroups control the amount of resources utilization, Memory, CPU, etc. It associated the process with its required resources.

### Namespaces

Namespaces provide isolation for processes. Each process in the namespace will have a unique id and is unaware of processes running in other namespaces.

### UFS - Unified File Storage

UFS enables you to combine multiple storage devices and behaves like single storage. Let's say you have a CD ROM with read access and a Hard disk with write access UFS lets us merge these two as a single storage unit that supports both read and write.

UFS in Docker is the core of keeping it lightweight. When running a Docker container, instead of creating a copy of the whole image with its files, Let's say (3 GB), Docker creates a copy-on-write layer that has access to all the files.

---

Docker is one of the most powerful tools to ship and deliver software. While celebrating that, we shouldn't forget the predecessor inventions that went in at the OS level that made Docker possible
