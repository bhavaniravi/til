---
added: Apr 01 2023
draft: false
image: null
layout: ../layouts/BlogPost.astro
slug: get-started-with-docker-compose
sub_title: By Building and hosting a full stack application
tags:
- devops
title: Get started with Docker-Compose
---

# Get started with Docker-Compose

Docker-compose is your tool of choice when you want to run more than one Docker container at a time, like in a full-stack application with a backend, frontend, and DB. In this blog post, we'll explore how to use Docker Compose to run a web application consisting of a frontend application built with React, a backend API built with Python Flask, and a PostgreSQL database.

### The Docker Compose File&#x20;

The first step is to create a Docker Compose file that defines the services for the application. Create a file called docker-compose.yml in the root directory of your project and add the following services:

```yaml
version: '3.9'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - POSTGRES_HOST=db
    depends_on:
      - db
  db:
    image: postgres:latest
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=mydatabase
```

In this configuration, we define three services: `frontend`, `backend`, and `db`. The `frontend` and `backend` services are built using Dockerfiles in the `./frontend` and `./backend` directories, respectively. The `db` service uses the latest version of the PostgreSQL image.

### Run the Application&#x20;

To run docker-compose application, navigate to the root directory of your project and run the following command:

```bash
docker-compose up --build
```

This command will start all three services and build any necessary Docker images. The `--build` flag ensures that Docker Compose builds new images if necessary.

You can also build the application using&#x20;

```bash
docker-compose build
```

Using the Application Once the application is running, you can access the frontend application by visiting `http://localhost:3000` in your web browser. The backend API is available at `http://localhost:5000/api`.

Connecting to the Database The PostgreSQL database can be accessed using a PostgreSQL client or any PostgreSQL-compatible ORM. To connect to the database, use the following connection string:

```bash
postgresql://myuser:mypassword@localhost/mydatabase
```

This string assumes you have defined the environment variables for the PostgreSQL username, password, and database name in your Docker Compose file.



That was a quick walkthrough to set up your app with docker-compose