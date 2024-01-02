---
title: How to Connect to Custom Oauth2 Provider Using Auth0?
sub_title: Using Auth0 to connect to different kinds of Oauth2 providers
slug: custom-oauth2-with-auth0
tags:
  - software-engineering
featuredImgPath: https://i.imgur.com/SBTXhe3.jpg
isexternal: true
published_date: 2021-08-24T00:00:00.000Z
created_date: 2021-08-24T00:00:00.000Z
draft: false
description: >-
  Oauth2 is an authentication protocol that allows external applications to
  access user data or act as a user. Auth0 is easy to implement, adaptable
  authentication and authorization platform. It, by def
---

# How to Connect to Custom Oauth2 Provider Using Auth0?

## What is Oauth2?

Oauth2 is an authentication protocol that allows external applications to access user data or act as a user. Here are a few examples to grasp the OAuth concept

1. Tweet Scheduler - An application where the user writes and schedules the tweet for a specific date and time
2. Calendar bot - A bot on top of Google calendar that will accept or reject calendar invites based on a predefined schedule

In both cases, the application acts as a user and performs the action(Tweeting/Accepting the invite) for them.

## How does Oauth2 Works?

1. The client application registers itself to the OAuth provider. In the case of Tweet scheduler, the application is registered with Twitter
2. When a user starts using the client application, they are requested to authorize the application to act on behalf of the user
3. Once the user approves and provides necessary permission, an access\_token is generated with expiry
4. This access\_token will be used by the client application in the future to perform actions on behalf of the user

## Auth0 and Oauth2

Auth0 is easy to implement, adaptable authentication and authorization platform. It, by default, provides connectors to authenticate with major applications.

![](https://i.imgur.com/L4S6Hiz.png)

Connecting to these existing platforms is as simple as filling out a Google Form. But recently, I worked with StackExchange, which is not an direct provider for Auth0. To support applications not listed in the providers, Auth0 has a generic connector. For the rest of the blog posts, let's see how to configure and connect them.

![](https://i.imgur.com/OvQ6H40.png)

## Connect to Custom Oauth2 Provider

### Step 1 - Creating Auth0 Application

Start by creating an Auth0 account. After sign up, Auth0, by default, creates an application for you. The settings screen will have basic app information. Look for `Domain` and make a note of it.

![](https://i.imgur.com/JRIo9ba.png)

### Step 2 - Register the application with OAuth Provider

For this blog post, we will be using StackExchange as our Oauth provider. Depending on the provider, you need to follow their Oauth2 documentation to [register your application.](https://stackapps.com/apps/oauth/register) StackExchange authentication documentation provides.

Any Oauth2 provider will ask for the following information.

1. Client name and description
2. Domain name of the client

![](https://i.imgur.com/FRL03nj.png)

Some providers might ask you to wait for a couple of days to validate your application. Once the registered application is ready, note down the `Client ID` and `Client Secret.`

### Step 3 - Create a Custom connection in Auth0

On the Auth0 dashboard, click on social connection -> New Connection -> Scroll down to see [Custom connection](https://manage.auth0.com/dashboard/us/thelearningdev/connections/social)

![](https://i.imgur.com/zmcKXuJ.png)

All the information required to create the connection can be found in the provider's [(Stackexchange's) Documentation](https://api.stackexchange.com/docs/authentication)

![](https://i.imgur.com/yjPZLCd.png)

### Step 4 - Fetching User Profile

The major difference between a pre-existing provider vs. a custom provider is the ability of Auth0 to fetch user information. Since the API response of the custom provider can be in different formats, you need to write a small node snippet to read the response and return the access token.

Auth0 provides you a snippet of the `fetchUserProfile` function, which will be called with the acess\_token once the user approves the client to have certain permissions. Using this token, you need to call the user profile API to return `user_id` and `email`(optional)

While the snippet provides a basic skeleton, you need to customize it according to the API and responses of the provider API.

For, e.g., In the case of stackoverflow, the APIs return a zipped response. Hence the responses should be unzipped before parsing it to JSON. Spend some time reading through the comments on the following snippet

```
function fetchUserProfile(accessToken, context, callback) {

    // import required libraries
    let https = require('https');
    var zlib = require("zlib");
    const querystring = require('querystring');

    // construct query string for fetch_user API
    let qs = {
        "site": "stackoverflow",
        "key": "<ACCESS_KEY>",
        "access_token": accessToken
    };
    qs = querystring.stringify(qs);
    let stackOverflowUserURL = 'https://api.stackexchange.com/2.3/me?' + qs;


    // make a GET API call
    https.get(stackOverflowUserURL, function (response) {

        let gunzip = zlib.createGunzip();
        let jsonString = '';

        // unzip and stream the API response in chunks
        response.pipe(gunzip);
        gunzip.on('data', function (chunk) {
            jsonString += chunk;
        });

        // once the stream ends convert it to JSON and return user profile info
        gunzip.on('end', function () {
            let bodyParsed = JSON.parse(jsonString);
            const profile = {
                user_id: bodyParsed.items[0].user_id,
                email: null
            };

            callback(null, profile);
        });
        gunzip.on('error', function (e) {
            callback(e);
        });

    });
}
```

Save the changes at the bottom of the screen.

### Step 5 - Debugging The Errors

Life would be much better if every snippet of code worked at first shot. But it doesn't. So how do you run the code? How to debug in case of an error? Where do `console.log` statements appear?

To provide all this, Auth0 has a [Weblog Extension](https://auth0.com/docs/extensions/real-time-webtask-logs). This extension logs all the messages when running the above snippet. Which comes real handy while debugging. Enable this extension before testing the connection

### Step 6 - Testing The Connection

To test the connection, click on `Try Connection` at the top of the screen. If everything worked well so far, you would receive an `It works!` message.

![](https://i.imgur.com/EmKOUHj.png)

***

{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}
