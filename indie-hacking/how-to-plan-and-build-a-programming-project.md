---
description: >-
  Internet keeps throwing this advice of "Build projects" to beginners, but
  "what?" & "How?" This article attempts to answer that question
---

# How to Plan and Build a Programming Project

_The blog is a WIP. I will finish soon and publish it_

You want to learn to program, pick a tutorial online, and they will teach you the basics. Now you got good with syntax. But when writing a simple for loop, you get stuck. You look for solutions online, and people suggest _"Build projects"._ Instead of fixing your 1st problem, they now give you a new problem.

I'm not saying "Build projects" advice is bad. I also received the same advice when I was in college, but there are a lot of missing pieces to this broad advice. No one tells to what to build and, more importantly, how to build. But wait, what about online courses?

I'll tell you exactly how it goes. You search udemy for "Python Project based learning" and get a list of courses, each teaching anything from 10-100 projects. You will purchase the one with the best reviews and good content

3 things might happen next.

1. The first two lessons will be a cakewalk; there will be a sudden jump in concepts, and you will feel lost.
2. Three weeks into the course, you will lose all the enthusiasm to build
3. You will finish the project and feel super accomplished, but... You will feel stuck when you open your code editor to do your own project.

Building projects on your own need a little more than just programming skills. Because of the lack of these fundamental concepts, "project building" feels like a humongous task. In my 5 weeks PythonToProject bootcamp, I teach a mental model for project building which can be extrapolated to build any backend Python project. This post is to share that mental model

### What to Build?

People kept asking me to build a project. But no one ever told me what a project is or how big it should be.

The project's goal in the learning phase can be as simple as a piece of code that will introduce you to new concepts and harden your skills.

It can be as simple as a

* Todo list app
* Calculator app
* Grocery list app
* Weather app

Or as complex as

* E-commerce application
* Streaming app
* Chat app

### But simple apps won't help me get a job

That's a valid fear to have, and it is true too. Recruiters don't take todo apps into account. But remember how you learned to write English? First, you learned the alphabet; you drew lines on top of what your parents or teacher drew, then learned to say words, form sentences, read more and eventually write your beautiful essay. That is exactly what this phase is sharpening your tool kit.

### Where to Start?

Now that you have picked a project to build, where do you start? Should you directly open the code editor and start churning out code? That's the next point I want to make. Opening the code editor the moment you have a project idea will work after you have developed the mental model for design. But as a beginner, planning your project before writing any code is better.

### How to Plan your Project?

Take a blank sheet of paper and answer the following questions

#### Scoping

1. Who is going to use your project?
2. What does the final version of the project look like? Get ambitious and list down every possible feature that you can think of
3. What does version 0.1 of the project look like? Shrink down your ambitious goals and discover 2-3 features you can build to make the project functional.

#### Design

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p>An ER Diagram created by one of my students for their V0.1 of whishlist app</p></figcaption></figure>

1. For each feature, think about the user flow. What will the UI look like? where does the data come from? where does it get stored? How is it consumed?
2. Know the tech&#x20;
   * This is where most people get stuck because they lack research or knowledge of what existing systems are available.
   * Want to store data? When to use DB vs. S3?
   * Want to raise notifications? Message Queues?
   * Authentication? JWT? Cookie-based? Session-based?
   * Monolith or microservices?
   * What are the pros and cons of these methods?
   * When to use what?

#### Detailing

1. Details, Details, Details
   * Once you've made the technology choices, you can get one step deeper
   * For each user, the action writes down which component will handle it. Frontend, backend, DB?
   * Draw a flow or a sequence diagram&#x20;
2. Think in code.
   * Now is a good time to think about the classes and functions you will write to achieve each of the above details.
   * &#x20;Start small with a single file and move things around as it grows.

### How to Build Your Project?

Once you have a good idea of what you will build, start building. Write those functions and classes. Execute them, and expose them as APIs.&#x20;

You're far from thinking about features; you're thinking about events and actions.

Use Git and Github to showcase each step. This will be a personal learning log but also serves as a way of showing your thinking process.

### Don't forget the Deployment.

These are the steps all hobby-project builders miss. It's great that your app works on your local machine. But production challenges never appear unless you deploy them in a system outside your machine. Until this step, all the components will be running in the same system. But the moment you think about deployment few questions arise.

1. Where are we going to host it? Should we use a Platform like Heroku for seamless hosting or get a bare metal machine?
2. Where is the DB going to go? Are we going to use a managed version or self-host them?
3. Are we going to use Docker?
4. How to check if there is an error?

See how quickly you've moved from a coding brain to a software engineering brain. That's the power of deploying applications.

To experience all of these through practical steps on your idea,&#x20;

### [Join PythonToProject bootcamp](https://bhavaniravi.gumroad.com/l/LaFSj)
