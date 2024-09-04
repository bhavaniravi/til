---
added: Sep 19 2022
created_date: 2019-08-01 00:00:00+00:00
draft: false
featuredImgPath: /media/async-task-python.png
image: null
unusedLayout: ../layouts/BlogPost.astro
published_date: 2019-08-10 00:00:00+00:00
slug: asynchronous-task-execution-in-python
sub_title: Schedulers became major architechtural component of any software that we
  use, these asynchrous task executors are behind the emails and notifications, the
  pop up that greets us on logging in, the repo
subtitle: Understand the software behind your social media notifications
tags:
- python
template: post
title: Asynchronous Task Execution In Python
---

# Asynchronous Task Execution In Python

Schedulers are a beautiful piece of code. In computer systems, they are as old as operating systems. In real world they are as old as our alarm clocks. In the world of computers, programmers used to schedule an appointment with an operator(a person) to run their code. Later when programmers wanted to take the operators out of their job they wrote scheduling algorithms.

When Operating Systems came into the picture, instead of computer operators it was schedulers that fed programs into the CPU for their execution. Over the years, the number of processing cores increased and so did the complexity of scheduling algorithms. The layers of hardware caches, RAM and hard disks brought up the need for different kinds of scheduling long, medium and short term.

Now, in the era of cloud and distributed systems, schedulers became an indisposable architectural component of any software system. These asynchronous task executors are behind the emails, notifications, the pop-ups that greet us on logging in, and reports that are sent to your email and so on.

Celery, RabbitMQ, Redis, Google Task Queue API, and Amazon's SQS are major players of task scheduling in distributed environments.

The rest of this blog sheds light on conventional task queue systems, and where asyncio stands, and finally we cover the pros on cons of the major players.

## Traditional Task Schedulers

Conventional tasks queues have two programs (a producer and a consumer) with a database acting as a queue. For every task created by the producer an entry is made in the database with a flag `NotStarted`, `Running`, `Completed`, `Failed`, and so on. At any point task workers (say a never-ending python program) will query this DB and look for incomplete tasks and start running it. It is a simple implementation but it has its own disadvantages.

**Disadvantages**

- Maintaining tasks on a DB table means that the table grows based on the number of tasks. It becomes complicated when the DB grows so much that we have to deal the problem of scaling.
- For every consumer that's free it queries the DB with task flag `Scheduled`, to fetch a scheduled task that it can run. The querying becomes costly as the size of the DB grows.

## Cron

Cron is the simplest software utility that enables you to run a task asynchronously at a given time. The utility maintains a single file (a table) called **crontab**. The utility itself is a scheduled job that runs every minute, takes a log of every command that is scheduled to run in the current minute, and runs each command. How cool is that?

### Usecases

1. Backups
2. Cleaning up temp files
3. Reminders

### Example

I wrote a simple python script to trigger a Mac notification that asks me to take a break every 20 minutes.

```
import os

def notify(title, text):
    os.system("""
    osascript -e 'display notification "{}" with title "{}"'
    """.format(text, title))

notify("Take a break", "You are sitting for too long")
```

```
# > crontab -e
*/20 * * * * python /<path_to_script>/notfication.py
```

### Problems to remember

**1. What if you have users across timezones?** Whenever we deal with time, we are also dealing with timezone problems. Cron jobs by default runs in the configuration of timezone in the machine it is running, we can override it using `TZ` environment variable. But cron isn't suitable if we want to run different tasks at different timezones.

**2. What happens if a cron fails?** When a script fails on executing a cron job, the error is just logged and the cron waits for the next schedule. This is not the most reliable way of handling errors. We would often want schedulers to retry until a certain threshold before moving on.

**3. Scaling** - What if the number of tasks to be executed at a given time is very large? - What if a single task occupies a lot of memory?

## Code Example - Treasure Hunt

I will be using a treasure hunter program as an example to explain the concepts in the blog. The problem statement is simple.

1. We have a treasure hunt program with 10000 files with one file containing a word `treasure`.
2. The goal of the program is to go through the files and find the treasure.

```
# Create treasure
def creating_treasure():
    """
    Creates N files with treasure randomly set in one of the files
    """
    treasure_in = randint(1, N)
    for i in range(0, N):
        logging.debug(i)
        with open(f"treasure_data/file_{i}.txt", "w") as f:
            if i != treasure_in:
                f.writelines(["Not a treasure\n"] * N)
            else:
                f.writelines(["Treasure\n"] * N)
    print (f"treasure is in {treasure_in}")
creating_treasure()
```

## Asynchronous Python

Asynchronous Python is gaining popularity after the release of asyncio. Though it has got nothing to do with task schedulers, it is important to understand where it stands.

### Threading

Python threading is an age-old story. Though it gives an idea of running multiple threads simultaneously, in reality it doesn't. Why? Because cpython has GIL(Global interpreter locks). Unless your program has a lot of waiting over external (I/O) events, using threading is not of much use. Even when your laptop has multiple cores, you would often find them idle on CPU intensive tasks due to GIL.

The `treasure_hunter` program implemented using threading would have threads looking through different ranges of files.

```
N = 10000
treasure_found = False
num_of_threads = 10
count = int(N/num_of_threads)
```

We have a common flag `treasure_found` for all threads to set.

```
def find_treasure(start, end):
    logging.debug(f"{start}, {end}")
    global treasure_found
    for i in range(start, end):
        if treasure_found:
            return
		with open(f"treasure_data/file_{i}.txt", "r") as f:
            if f.readlines()[0] == "Treasure\n":
                treasure_found = i
                return


start_time = time.time()

threads = [threading.Thread(target=find_treasure, args=[i, i+count])
           for i in range(0, N, count)]
[thread.start() for thread in threads]
[thread.join() for thread in threads]

print("--- %s seconds ---" % (time.time() - start_time))
print (f"Found treasure {treasure_found}")
```

### Multiprocessing

The multiprocessing module enables us to overcome the disadvantage of threading. The simplest way to understand this is that the GIL applies only to threads and not to processes, thereby providing us a way to achieve parallelism.

Multiprocessing also works well on CPU intensive tasks as we can use all the cores available independently. When designing a multiprocessing problem, the processes often share a queue from where each process can load tasks for its next execution.

```
num_of_process = 100

start_time = time.time()
processes = [Process(target=find_treasure, args=[i, int(i+N/num_of_process)])
             for i in range(0, N, int(N/num_of_process))]

[process.start() for process in processes]
[process.join() for process in processes]

print("--- %s seconds ---" % (time.time() - start_time))
print (f"Found treasure {treasure_found}")
```

### Asyncio

In the above two examples, the switching between the threads or processes is handled by the CPU. In certain cases, the developer might be more aware of when a context switch should happen over CPU. Instead of spinning up processes or threads, it lets the program(developer) decide when a program can halt and leave a way for the execution of other tasks.

```
async def find_treasure(start, end):
    global treasure_found
    for i in range(start, end):
        if treasure_found:
            return
        # Await until file is read
		await read_file(i)


async def main():
    tasks = [find_treasure(i, i+count)
            for i in range(0, N, count)]
    await asyncio.gather(
            *tasks
    )

asyncio.run(main())
```

## Celery

> Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation, but supports scheduling as well.

Celery works around two primary components a `Queue` and a `Worker`. `Queue`, also called as `message_brokers` is a queuing system where you push your tasks to be executed asynchronously. `Worker` pings the queue once in a while and executes the tasks.

**Message Broker**

You might often confused between the terms `Redis`, `Celery` and `RabbitMQ`. The `Queue` component mentioned earlier is not inbuilt in celery. It uses `RabbitMq` or `Redis` queuing system. This is why you often find articles that mention all of them.

**Worker**

When you start a `celery worker`, it creates a supervisor process which in turn spins up a bunch of other `executors` these are called `execution pool`. The number of tasks that can be executed by a celery worker depends on the number of processes in the execution pool

**Scheduling Tasks in Celery**

Unlike crontab, celery by default does not schedule tasks to be run at certain times. To support job scheduling, celery uses Celery Beat.

**What happens when a task fails?** When a particular task fails, you can configure celery to retry until a particular exception occurs, or set `max_retries` parameter to enable retrying `n` times before giving up.

**Idempodency**

Let's say you are backing up `N-items` into a DB as your task. In case two workers pick up the tasks and execute it then it is for the calling function to make sure that the same entry is not made in a DB twice. Workers will have no clue about the side effects of running a particular task.

## Redis Queue

Redis by default is an in-memory database and that's about it. RQ (Redis queue) is a task scheduler to asynchronously execute tasks, which uses redis' `Queue` data structure and has an inbuilt worker implementation. The architecture and working is very similar to that of Celery.

```
N = 10000
num_of_process = 10
count = int(N/num_of_process)

start_time = time.time()
q = Queue(connection=Redis())
results = [q.enqueue(find_treasure, i, i+count)
           for i in range(0, N, count)]
```

**RQ vs. Celery**

1. What if one fine day you wake up and decide to change your Queueing system. Celery supports an extensive line up of message brokers but RQ is built only to work with `Redis`.
2. Celery supports subtasks. RQ doesn't.
3. RQ works with priority queues and you can configure workers to work on tasks with a certain priority. In celery the only way to achieve this is by routing those tasks to a different server.
4. RQ is only for python, Celery is not.
5. Celery supports Scheduled jobs.
6. RQ workers will only run on systems that implement `fork()`. Most notably, this means it is not possible to run the workers on Windows without using the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about) and running in a bash shell. If you are using windows, RQ is not for you.

## RabbitMQ

RabbitMQ is just a queuing system. It is built over AMQP protocol. In comparison with Celery (which only has worker) and RQ (has both worker and Queue), RabbitMQ has just the queueing system, a robust one.

#### Architecture

### Components

RabbitMQ works on publisher subscriber model. It has 4 major components.

**Producers** - The code that pushes tasks to the queue. **Exchangers** - Decides which queue a message should be pushed into. - Direct (Send a message to the queue with respective table) - Topic (Send a message to the queue that matches a specific routing pattern) - Fan out (Send a message to all queues) **Queues** - Queues are what we have been discussing so far. It has a list of tasks for the workers/consumers. **Consumers** - Consumers (Worker), also called as workers, are responsible for the actual execution of tasks. At any point of time, workers can be configured to work on a specific queue. RabbitMQ does not have it's own worker, hence it depends on task workers like Celery.

> Fun Fact RabbitMQ, inspite of supporting multiple queues, when used with celery, creates a queue, binding key, and exchange with a label `celery`, hiding all advanced configurations of RabbitMQ.

**Pros**

1. Wonderful documentation
2. Supports multiple languages
3. Messages executed can be acknowledged

**Cons**

1. Difficult to trace and debug
2. Errored queues are stored in a different queue
3. Does not support priority

## Google Task Queue

Google Task Queue provides two types of queueing mechanism.

1. **Push Mode** - The workers dequeue tasks pushed into the queue.
2. **Pull Queue** - Your code is responsible for dequeuing the task from the queue and executing it.

## Google Pub/Sub

While Pub/Sub is close to asynchrous execution, Google PubSub primarily focuses on message queues and streams. Imagine sending a group message or posting something in a facebook group then every subscriber who is listening to that specific queue should get an alert. These are classic usecases of a Google Pub/Sub.

#### Where does it differ?

At this point it is valid to ask, why can't we implement the Pub/Sub model with Task queue, both are asynchronous and both execute tasks right? Google provides us with a clear distinction

## Choosing between Cloud Tasks and Cloud Pub/Sub

Both [Cloud Tasks](https://cloud.google.com/tasks/docs/dual-overview) and [Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/overview) can be used to implement message passing and asynchronous integration. Although they are conceptually similar, each is designed for a different set of use case. [This page](https://cloud.google.com/pubsub/docs/tasks-vs-pubsub) helps you choose the right product for your use case.

### Key Differences

The core difference between Cloud Pub/Sub and Cloud Tasks is in the notion of implicit vs. explicit invocation.

> Cloud Pub/Sub gives publishers no control over the delivery of the messages save for the guarantee of delivery. In this way, Cloud Pub/Sub supports **implicit** invocation: a publisher implicitly causes the subscribers to execute by publishing an event. By contrast, Cloud Tasks is aimed at **explicit** invocation where the publisher retains full control of execution. In particular, a publisher specifies an endpoint where each message is delivered. In a nutshell, Cloud Tasks are appropriate for use cases where a task producer needs to defer or control the execution timing of a specific webhook or remote procedure call. Cloud Pub/Sub is optimal for more general event data ingestion and distribution patterns where some degree of control over execution can be sacrificed.

## Resources

I referred to a whole bunch of links and read through all the documentation before writing this blog. Here are a bunch of blogs that I really enjoyed.

1. [Asyncio in Python](https://realpython.com/async-io-python/)
2. [Python Concurrency](https://realpython.com/python-concurrency/)
3. [Celery Execution Pool](https://www.distributedpython.com/2018/10/26/celery-execution-pool/)
4. [Celery and Celery beat Euro Python](https://www.youtube.com/watch?v=kDoHrFLkahA)
5. [https://www.youtube.com/watch?v=ztyyn7hmcJo](https://www.youtube.com/watch?v=ztyyn7hmcJo)
6. [Celery Vs RQ](https://stackoverflow.com/questions/13440875/pros-and-cons-to-use-celery-vs-rq)
7. [https://www.fullstackpython.com/task-queues.html](https://www.fullstackpython.com/task-queues.html)
8. [https://www.youtube.com/watch?v=nrzLdMWTRMM](https://www.youtube.com/watch?v=nrzLdMWTRMM)
9. [Google Task Queue vs Pub/Sub](https://groups.google.com/d/msg/google-appengine/IcIjLfgnNXs/-m_ik7h6DgAJ)
