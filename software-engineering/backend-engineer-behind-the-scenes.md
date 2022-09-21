---
title: Backend Engineer - Behind the Scenes
sub_title: What goes into building a backend system?
slug: backend-engineer-behind-the-scenes
tags:
  - software-engineering
featuredImgPath: >-
  https://lh3.googleusercontent.com/BrtspPWUUvqGlTyO6BJBzbZQeS7-KHRh48y5-8aD62Hk5t0Ab2CR8AeIYlfhEo-XUq3QmyeHbXnyVih_K0OrIuG2wyNfc8CcuFzG5odWUIyGLtJrbnb0UTTYUV1U1hqLcn4cJNwUPhU=w857-h643-no
isexternal: true
published_date: '2020-04-10'
created_date: '2020-04-10'
draft: false
description: >-
  The process of dissecting a complicated problem into solvable pieces is what
  makes this job so interesting and lovable.
---

# Backend Engineer - Behind the Scenes

Eight months back, when I crafted my backend skills well at Orangescape. I wanted more. I started looking out for other opportunities. So when I interviewed Saama technologies, I told [Malaikannan](https://www.linkedin.com/in/malaikannan/), my current manager, that I want to work on challenging projects. He promised that I would work on things, where Google searches won't be enough. Six months and three complex projects later, I think he took the promise way too seriously. I want to share what happens behind the scenes when I build backend systems because it's so much fun.

## Why now?

Why not write this post three months back when I cracked my first project?

The first project might have been a one-time incident. One can share a framework only when a pattern repeats more than once.

## What do I do?

tl;dr - I am a part of a team that figures out whether the crazy ideas of our product managers are achievable or not.

I work for the R\&D division of [Saama Technologies](https://www.saama.com/), with some of the brightest minds you can find. I call them _"the brainy bunch"_. NLP, Deep Learning, Chatbots, Devops, Quantum computing, AutoML, name an upcoming technology, we got one on our team. We build as platforms and expose them to the Saama Engineering team for them to incorporate it with our core products.

## Behind the Scenes

### Birth of a Project

Product managers, one morning after waking up from sleep, Just kidding!, after having a million interaction with customers and seeing an impossible request arising continuously, comes to Malai(my manager). On Malai's input, the project gets handed over to us.

One such impossible request and hand-over call later. I had this project at hand.

### First 3 weeks

The first three weeks are crucial because there is uncertainty everywhere. Neither your brain nor the manager or the product owner has answers to all the questions. Imagine walking in the dark or finding your way through a forest without a map.

During this time, I can't devote to anything else. You won't see me tweeting, writing a blog post, or working on side projects. The brain will be occupied entirely by

* What the hell is this?
* Why am I doing this?
* What am I doing wrong?
* Why the hell is it so hard?
* Why don't people write documentation?

Few things I do at this part apart from doubting myself is

* Reading through the requirements and user stories like the bible.
* Staring at the wall for hours and visualize the flow
* Sketching the ideas after ideas
* Share them visualization with your teammates to validate and iterate
* Million Google searches
* Check if the technology choice accommodates all the requirements

### The Spark

At the end of 2 to 3 weeks, the visuals of the control flow look like a possible target to achieve. You will no longer hate yourself much; you won't feel that stupid.

For example, The current project involves a total of 7 components/services. We got to build 3 out of 7 components ground up. The rest of the components already exists, eg., Kubernetes, Docker, Airflow. It's the matter of bringing them all together.

Sounds easy, right? Now that I look at it, yes, it is not so hard. But two weeks back, I had the tiniest clue what the six components did, whether they had the necessary functionality. It took me two weeks to understand if the six components match the requirement. The flow diagram on the paper had gone through 4 iterations last week.

Finally, it is the matter of converting the flow diagram into the lines into lines of code. Even now, there are few missing pieces, but the confidence of coming this far will power things through.

### The Development

The most straightforward segment of software development stages is to convert your ideas into code. Of course, no design is set in stone. There might be decisions that you might have to take on the fly. But there are a few things that you can't get wrong.

#### Writing good code

Following the standards(Linting, documentation, naming conventions) should always be your priority

#### Test-Driven Development

A project as complicated the one I am building is bound to change, so it is essential to make sure your test suite is created along with the codebase.

#### Deployment scripts

Trust me on this, if you have Docker and Kubernetes involved in your production, make it a habit to set it up on Day 1 and test your code there. Saves hours of debugging later.

#### Dissecting your technology choices

It is an essential step before starting development. Create a checklist of things expected from your technology choices, create a matrix of what's supported and what's not. It is important to understand where things won't work than where things will.

While you can get away with Stackoverflow-ing but, be ready and open to read beyond documentation and other codebases.

#### Avoid spec/architecture change

Changes at this point are costly. Mostly because you have to work through another 2 weeks of uncertainty. So don't start coding until the product owners are sold on your architecture design

#### Integration testing

While unittest gets you through module-level stability. Any software is never complete without components working in harmony, so add doses of integration tests

#### Performance

Always keep performance in mind. When we talk about performance, think of latency(time taken for 1 task to complete) vs. Scalability(No of tasks completed per sec)

It is tempting to jump in and fire those git commits but what's going to save you significant time is the time you spend on designing is what makes development a smooth experience.

### Pre & Post Production

The crucial step of any software product is taking it to production. I am not a pro at the following but from what I learned from my peers these are the things that you would keep tabs on.

#### Continuous Deployment strategies

Once things hit production, you would want to move fast, be it bug fixes or new features things start to roll, and the stakes are high. Hence having a solid CI/CD pipeline comes handy

#### Security and Compliance

The projects of Saama involves high confidentiality, therefore following the compliance guidelines and keeping the team aware of it is crucial

#### Monitoring and Logging

The turn-around time to find and fix things in production is short. That's when a reliable tracking and logging framework comes handy

#### Documentation

Document every piece of your production setup. It can be a bunch of ansible scripts with setup guidelines.

#### Risk management

What's the backup strategy, how to handle when a particular cloud-zone goes down, what's your business continuity plan during calamities

### Learn, Unlearn, Repeat

Post-release as the users start using the product bug counts are bound to increase. As far as you have done everything above right, you can cross your fingers and hope nothing big pops up. Once the bug count saturates on the product/feature is adopted well, you can roll up your sleeves and walk up to the product owner for a new set of challenges. Oh, wait! You already have a call scheduled to discuss just that.

None of this might sound easy or humanly possible. Yes, there are deadlines, uncertainties that put pressure on you. The process of dissecting a complicated problem into solvable pieces is what makes this job so exciting and lovable.
