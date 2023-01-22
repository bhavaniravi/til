# How to Design a Chatbot System Architecture

### Requirements

- Incoming user messages need to be responded to in order.
- Conversations should be persisted as part of the bot.
- An administrator should be able to view conversations users have with the bot.

### Objective

A) Create an overview of the system to explain to a non-technical person how it works. What are the advantages and disadvantages of your system?

B) We want to scale the system to handle thousands of users at the same time. How can we scale the above system? Create an overview of the system to explain it to an internal development team.

### Pre-condition

- No system exists currently and we are building one from scratch
- No technological constraints, the team is equipped to choose the stack
- Facebook webhook calls are HTTP and should be responded in 20 seconds, if not, a messenger would retry until it gets a 200 response.

### Architecture

![Workflow](https://i.imgur.com/6cvbRET.png)

### Workflow

- API Gateway passes on the incoming request from different clients to respective service
- The chatbot server takes in chat messages from different clients and provides a response.
- The NLU engine is responsible for predicting the intents and entities from a given text
- The Chatbot server also acts as an action server that calls external APIs to perform a specific action
- Chatlog service is responsible for logging all the messages in the system.
- Redis store is responsible for maintaining the state of the messages for each user

![](https://i.imgur.com/qO4lKql.png)

#### State management

Redis store maintains a queue for each individual user's messages

1. On receiving a user message, check if there is a queue on Redis for the specific user_id, and the request for the same `(user_id, message_id)` is not previously requested. If yes push the message to the end of the queue
2. Wait until a specific timeout to see if the `message_id` has moved to the front of the queue
3. If the state of item_at_front_of_queue != processing (ie., no other server is processing that message), process that message
4. If the queue is empty, push the message to the queue, mark it to state **processing** and process the message
5. On processing remove it from the queue

### Chatbot Log

![](https://i.imgur.com/EYOu3e9.png)

The chatlog is designed in such a way

- Capture different message types, images, links, text
- The timestamp in input and response can provide us with insights like `avg time taken to process a message`
- The intents and entities are mapped to the response, which can be used when retraining the bot

#### Scaling

- As you can see, individual components of the system are bounded in scope and functionality
- As the system scales, we can employ Redis sharding to handle chunks of user
- The servers will have load balancers horizontally scaling the containers/pods depending on the traffic

#### Advantages

- Since we employed microservices, Each module is scalable independently
- No two messages of the same user will be processed twice
- Extending the system to support other chat clients is supported.

#### Disadvantages

- Does not support multi-tenant
- The follow-up messages from a specific user might have to wait if a message is already processing, resulting in client timeouts.

### Architecture - Non-tech users

#### API Gateway

API gateway is the equivalent of a receptionist in an office. When an external request comes in, the receptionist knows whom to route the request to. The same is applicable to the API gateway.

This ensures

- All the Authentication are captured in one place.
- Provides a single interface for the outside world.

#### Chat Server

The chat server is the core module of our system responsible for replying to all incoming messages. Imagine a chat server as a customer service executive who collects information from different sources and provides a suitable response to a user query.

#### Redis Store

Redis storage(State management) works like a kanban(Trello) board, A central place where we track the state of all the messages. According to our business constraint, two messages from the same user should not be worked on simultaneously. Hence, Each user's message is tracked in a separate queue. The message is processed when it reaches the front of the queue.

### Architecture Evolution

#### **A simple client-server architecture**

Although relatively simple, when we scale the system to run multiple servers to handle large traffic, we might end up processing messages of a specific user parallelly, resulting in a mismatched context

#### **Event-Driven Architecture**

Given the requirement of `preserving-order` Queues are the only way to achieve it. (2) ensures all the incoming messages are entered into a queue, and the processor processes each message from the queue

- This might work for websocket-based systems, but since Facebook messenger is HTTP and expects a response in 20 seconds, we can't hold on to the messages in a centralized queue.
- Adding a centralized queue doesn't ensure two different servers are working on the same users message

#### **Event Driven + Persistence**

> Adding a centralized queue doesn't ensure two different servers are working on same users message

To avoid this disadvantage, it was clear that we need a centralized persistence layer that all the servers can refer to. Hence thought of having a centralized DB that tracks the state of every message

- The DB reads and writes will be massive and costly as the traffic increases
- Still doesn't solve the queueing problem

**4. Persistence**

A Centralized Queue does not solve our problem, so we dropped it and kept the persistence(DB) alone. For each message, check the DB to see if any other message is in `processing` state

1. Again from the scalability aspect of it, is not a good idea to do a DB operation
2. If the message is found to be `processing` state, create an entry in the DB and wait until all previous messages are processed(which again is a DB query)

**5. Queue Upgraded**

Design 1.0 arrived from taking the best of 3 and 4. We need a queue to handle orders and centralized storage to track all the messages.

1. Redis Storage instead of a DB, making the system scalable for huge traffic
2. 1 Queue/User instead of a centralized queue

---

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
