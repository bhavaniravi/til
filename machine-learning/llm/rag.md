---
added: Aug 31 2024
description: null
layout: ../layouts/BlogPost.astro
slug: rag
tags:
- llm
title: RAG WTH Is it?
---

# RAG WTH Is it?
Retrieval Augmented Generation - Yet another acronym the ML researchers have slapped onto something so simple.
You have a large pre-trained model
You have data lying in your documents, PDFs, CSV files
How would you extend these models to infer insights from this data
or in simpler terms, How can you make LLMs answer questions about your employee agreement your blog posts, or the data that is super private to your company?
We can achieve it by performing 3 steps
 Retrieval
Augmentation
Generation
Get it? Hence the name. Very innovative.
----
Ok...Ok.. wait....this is what every article in every major AI company is telling you. 
I can go two routes from here 
Explain to you how to do it.
Again plenty of articles exist
I highly recommend this video 
https://www.youtube.com/watch?v=sVcwVQRHIc8
Explain some cool stuff I learned in the form of prompt engineering
Multi-query
Given a question, 3 other questions of a similar nature are generated and consolidated result is sent back
HyDE
Takes LLM to a party. Given a question HyDE generates a hypothetical answer and then uses it to search the document you have
Tokenization, and Vectorization are what I picked up during my chatbot days. I’m gonna leave them alone
Oh wait! 
LLamaIndex has them all
https://docs.llamaindex.ai/en/stable/optimizing/production_rag/
Take Diversion into the World of Monitoring
it all started with the video and LangChain. People hate Langchain for it’s abstraction. But I loved the level of tracing it supports
<LangChain image goes here>
Guess who else also does it
Sentry
Arize UI