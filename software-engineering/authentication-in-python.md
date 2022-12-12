---
slug: authentication-in-python
published_date: 2019-09-01T00:00:00.000Z
created_date: 2019-08-26T00:00:00.000Z
title: All About Authentication Systems
template: post
draft: false
subtitle: A blog to help you understand authentication systems in detail
tags:
  - python
featuredImgPath: /media/auth_systems/featured.png
description: >-
  Authentication is a concept of ensuring that the right people gets access to
  the information. The age old concept of lock and key has evolved into todays
  multi-variant authentication systems
---

# All About Authentication Systems

Authentication systems are the protective barrier of any software. It makes sure that right people enters the system and access the right information.

Though being the major component of an application, the chances of you building one from the scratch in the industries less, Unless you are working on a project from scratch. That being said, the most common advice in a hackathon is to not waste time implementing login page. Now as years go by and as you grow up the career ladder, it is important to understand how the whole system works to elevate yourself as an architect and make more educated design decisions.

## The Common Misconception

When thinking about authentication, the common imagery people have is a login HTML page submitting data to a backend API cross checking it with a data in a DB? Well, though it covers the bare bones of an authentication system. There is more to it which we would discuss in the rest of the blog.

1. Types of Authentication
   * [Basic](authentication-in-python.md#basic-authentication)
   * [Digest Based Authentication](authentication-in-python.md#digest-based-authentication)
   * [Cookie/Session Based](authentication-in-python.md#cookiesession-based-authentication)
   * [Token Based](authentication-in-python.md#token-based-authentication)
   * [SSO](authentication-in-python.md#sso)
   * [Oauth2](authentication-in-python.md#oauth2)
   * [Two Factor Authentication](authentication-in-python.md#two-factor-authentication)
2. [Authorization](authentication-in-python.md#authorization)
   * Access Control
   * Types Of Access Control
3. [Which authentication method to use?](authentication-in-python.md#which-authentication-method-should-you-choose)
4. [Designing a distributed auth system](authentication-in-python.md#authentication-in-a-distributed-system)

Before we move on…

> All data sent to clients over public links should be considered “tainted” and all input should be rigorously checked. SSL will not solve problems of authentication nor will it protect data once it has reached the client. Consider all input hostile until proven otherwise and code accordingly.

## Basic Authentication

It is the simplest of authentication mechanisms. It is a part of HTTP protocol. It is a challenge response scheme where the server challenges the client to provide necessary information to access the resource

### How does it work?

1. Get the username and password from user
2. Encode it using `base64` algorithm
3. Set it in the Authorization header and send it along each HTTP Request.

```
`Authorization: Basic XAAUVBBhHI87IO==`
```

### Advantages

1. Easy and simple to implement
2. APIs are faster since there is no complex encryption/decryption involved

### Disadvantages

1. Basic Auth implemented in a non-SSL (HTTPS) network is a huge security vulnerability.It is easy to decode an Base64.
2. Sending passwords over all the HTTP request provides a pool of requests for attackers to pick passwords from. Once they crack one the system becomes open for attacks.

## Digest Based Authentication

It is an upgraded version of Basic auth. It overcomes the security vulnerabilities of Basic auth over an HTTP network. We no longer deal with `base64` encoded strings, instead the server provides digest for the client to use while encoding the username and password. In digest base auth we no longer have to worry about universally known base64 encoded string.

> Note: This doesn’t mean it is ok to send passwords over non-HTTP network, it provides just a safety net if you do so.

### How does it work?

1. Request a server for a resource with no auth
2. Server sets the header with certain digest information
3. Get the username and password from user
4. Hash the username and password along with the digest send it to the server.
5. Server decodes the string with the digest and allows the user

### Advantages

1. Prevents passwords sent as plain-texts
2. Avoids [Phising](https://en.wikipedia.org/wiki/Phishing)

### Disadvantages

1. Digest method is still vulnerable to man in the middle attacks.
2. Client has to make 2 calls to get a resource, one to get digest information and another to login

## Cookie/Session Based Authentication

Cookie/Session based authentication is the most commonly used in web apps. Yes, both session and cookie are not exactly the same but the conceptually either the client uses a cookie/session to identify itself as a logged in.

### How does it work?

1. Get the username and password from user
2. Set it in request form params and send it to the server
3. Server validates the user based on the given username and password﻿
4. Once successful validation, create a cookie and set it in the response
5. The client then uses this cookie/session to make future requests.

### Advantages

* We no longer set the password in every request making the window for attacks smaller.
* Enables state maintenance in a stateless system. Cookies maintain the state that the user is already logged in.
* Can revoke the validity of a cookie anytime.

### Disadvantages

* Cookie based authentication is suitable only for Single domain system. If you want both a web and a mobile app or may be a separate client server, then you got to deal with CSRF.
* Prone to XSS and CSRF attacks since the cookie is available for other apps to read
* You need to store the session information in a DB which also brings in the question of scale

## Token Based Authentication

Token Based Authentication is a form of stateless authentication. Instead of sending email and password over for authentication we use a server generated token. Oauth, JWT, Open ID all comes under token based authentication

### JWT

#### How does it work?

1. User submits a username and password
2. Server validates and returns a singed token JWT
3. Use the token to allow future requests

#### Advantages

1. The server no longer have to bear the overhead of session information
2. No more CSRF. With token based auth you are dealing with a bunch of APIs consumed by different clients
3. Works well on microservices architecture.

#### Disadvantages

1. Cannot revoke the access to a user.
2. The safety of the token relies on the consumer of the token.

## OAuth2

Oauth2 is an advanced version of Token based authorization. Often we use Facebook/Google/Twitter to sign-in to an application. These are the examples of OAuth2.

### How does it work?

1. User sends an authentication request to say Google/Facebook.
2. On finding that the user has an account on Google, the Google server responds with an authorization grant.
3. The requesting application uses the authorization grant access specific information
4. On gaining the permission, the app generates an access token.
5. The client then uses the access token to access a resource.

## SSO

Personal computers are classic examples of an SSO system i.e., you enter password once and get access to all the apps. Google is another classic example you login to Gmail and get to use all the GDrive apps that comes along with it.

### How does it work?

1. Let’s say you are trying to access Google forms. Google sends a request to the forms, the forms of service inturns calls an authentication service to make sure that the current user is logged in
2. if the person is already logged in present with the information
3. If not show him a login screen to authenticate the user.

## Oauth Vs SSO

This sounds similar to oauth but, the major difference is Oauth allows only specific access to an app whereas SSO provides complete access of the data available

### Advantages

1. Talk about user experience your user needs to remember only one set of password
2. Secure, since a single service is holding your password and is responsible for its security

### Disadvantages

1. Single point of failure: When an authentication service goes down all the app relying on it cannot be accessed
2. Any security breach in the authentication system will open access to a wide set of apps and data.

## Two Factor Authentication

Two Factor authentication is a subset of multi-factor authentication. There are 5 broad classification of these factors

1. Knowledge Factors - Which city are your from?
2. Possession - OTP, Validation email
3. Inherent factor - finger print, eye ball scan
4. Location Factor - GPay
5. Time Factor - When system is allowed to access only at a specific time

## Authorization

Authorization is something that happens once the user logs into the system. Does an user have access to a specific information? For example, in a library the lenders need not know the billing/vendor information related to each book. In a system that involves more than one type of stakeholders, the authorization is as important of authentication.

### Access-Control

Authorization is achieved using access control, you can imagine it as a “Restricted Area” sign with a guard.

#### Types of Access Control

1. **RBAC - Role Based Access Control** - A user with specific roles can access specific data. E.g., Only a SuperAdmin can change the Locale of the system.
2. **MAC - Mandatory Access Control** - High security systems avail these kinds of access control
3. **DBAC - Discretionary Access Control** - The business data decides which information is available for a specific user. E.g., According to the business logic of a library application, only a library lender can only see books lent by themselves.

## Which Authentication Method Should You Choose?

1. Only Web Application - Cookie/Session Based
2. Expose APIs to user - Token Based
3. Web + Mobile Apps - Cookie and Token Based
4. Letting users login easily Oauth
5. Building apps on top of Google/Facebook - SSO

## Authentication In a Distributed System

In a monolithic application the authentication APIs are tightly coupled to the app itself I.e., we will have a single DB storing both the user information and the business data. In that case there is a single instance of a server responsible for authentication.

In a distributed system with microservices architecture the design becomes a bit more complicated.

Answering the following questions and understanding its pros and cons will help us land in an educated decision

### Authentication inside every microservice

Microservices architecture directly translates to independent services working together with that ideology in mind “Auth inside every microservice” looks like an anti-pattern. Though an advantage of this method is reduced latency, we would end up doing a bunch of redundant things at every server.

### Authentication system as a filter

If that’s the case with having auth service at each end and the auth system validates each request like a firewall. The drawback of this method is that auth service itself will become a bottleneck as the number of requests scales up.

### Global Authentication

The most commonly practiced method in microservice architecture where the authentication system sets a JWT token to the client and any request that made to the services are then cross verified with the Global system.

## Resources

1. [https://cybersecurity.ieee.org/blog/2016/06/02/design-best-practices-for-an-authentication-system/](https://cybersecurity.ieee.org/blog/2016/06/02/design-best-practices-for-an-authentication-system/)
2. [http://ijcsit.com/docs/Volume%207/vol7issue4/ijcsit2016070406.pdf](http://ijcsit.com/docs/Volume%207/vol7issue4/ijcsit2016070406.pdf)
3. [https://swoopnow.com/web-application-authentication-best-practices/](https://swoopnow.com/web-application-authentication-best-practices/)
4. [https://cheatsheetseries.owasp.org/](https://cheatsheetseries.owasp.org/)
5. [https://medium.com/@kennch/stateful-and-stateless-authentication-10aa3e3d4986](https://medium.com/@kennch/stateful-and-stateless-authentication-10aa3e3d4986)
6. [https://habiletechnologies.com/blog/pros-cons-using-authentication/](https://habiletechnologies.com/blog/pros-cons-using-authentication/)
7. [https://www.youtube.com/watch?v=zIhB8LuBA6g](https://www.youtube.com/watch?v=zIhB8LuBA6g)
8. [https://www.youtube.com/watch?v=SLc3cTlypwM](https://www.youtube.com/watch?v=SLc3cTlypwM)
