---
slug: challenges-in-full-text-search
title: Challenges In Full-Text-Search Systems
description: >-
  While Full-text-search is famous for search through documents at a faster
  rate, there are other intresting ways in which these systems handle scale,
  synonyms, abbrevations, misspellings etc., we will take an indepth view of the
  same in this blog
subtitle: An Indepth view of search problems and how Full-Text-Search Solves them
tags: ["software-engineering"]
---
# Challenges In Full-Text-Search Systems
Text problems are the most interesting ones to solve. From being a part of a CS Engineer’s academics to kick ass feature of a product, searching is everywhere. It doesn’t matter what language, database or Service you rely on, if you have a bunch of data your users will want to search through them.

Now that we know the necessity of search feature in an app, the struggle comes when your data grows. Ordinary regex or grep based search methods won’t hold good for this scale of data. Full-text search is more intuitive than just pattern matching. The main idea is to give the user with the relevant results. We need a swiss army knife a Full-text-search to solve our search problems. This blog will cover what Full-text-search and it solves those problems.

![Full-Text-Search Systems](/media/fts/fts-featured.png)

## What is Full-Text-Searching?
Full text search is an advanced method of searching through documents and DB records. While conventional searches use pattern matching(grep/regex) methods and scanning through the documents, full-text search promises fast retrieval of data with advanced indexing and more intuitive search results based on relevance.

## Why do we need Full-Text Search?

You tell me. Which is better looking for a book in each rack of a library or searching through a library management system and finding the rack/row number? Every Google/Amazon search we do is a Full-text-Search(FTS)

## How does Full-Text Search work?
The full-text search first starts with a DB containing a bunch of Data(documents). These data are indexed based on the words in the documents and stored. When a user enters a search query, the query is split into tokens and mapped across the built index to find the relevant documents

![Full Text Search using Apache Lucene (Part-Iii)](https://www.knstek.com/wp-content/uploads/2015/01/lucence-flow-1.png)

## Challenges In Full text Search
To understand and appreciate the mechanisms and terms involved in full-text-searching you need to understand the challenges involved in the same. A few of the common challenges are.

1. Scale - How does it work for huge amounts of data?
2. proximity - How to make the search results relevant?
3. Handling Synonyms, Abbreviations, homonyms, Phonetics
4. Handling misspellings
5. Searching through images
6. Re-indexing - Handling new or constantly changing data?
7. FTS is distributed Systems

## Scaling - Indexing the Documents

As we discussed conventional `grep` based systems no longer works at the speed, we need when the number of documents increase. Indexing is a method followed in most data stores for fast retrieval of data. You can imagine these as hash tables with a mapping between words and its associated document.

1. Take all the words from the documents and remove stop/noise words
2. Stem the words based on the language
3. Create a table of words mapping it to its occurrence in the document
4. On entering a search query tokenize, stem the words and cross check across the index. 

![Document Indexing](https://i.imgur.com/lcfDdQZ.png)

## Proximity - Word Vectors
Proximity is “how relevant your search results are?” to the search query. When talking about Proximity we often focus on finding the documents that relates to the “Intention of the user”.

For e.g., when searching for a white shirt, the color “white” carries a specific weight. 

The proximity is calculated by a relevance score using one of the following methods 
1. **Field Length Normalization** - Smaller the field size the more relevant for eg., “Item Name” has a higher weight than “Description”
2. **Frequency** - The larger the number of time a term occurs in a document more relevant .
3. **TF-IDF** - It’s the inverse of frequency which suggests lower the occurrence, higher the weights

Once documents are matched from the index a relevance score is calculated based on one of the above methods and the results are sorted according to this score.


## Abbreviations, synonyms, homonyms and Phonetics 
In the era of instant messaging we are used to use not only the accepted abbreviations like W.H.O but we also create ones of our own like TC and AFK. Now when searching for “world health” valid to bring out documents that mentions “W.H.O”. 

1. Search Thesaurus - Where a mapping all the abbreviations and its associated expansion is saved.
2. Text Normalization - On creating an index the abbreviations are normalized to its actual text searching on it works like searching over an actual text.

## Searching Through Images

Gif-search is an example of Full text search in images. Google Images works based on the relationship between a blog post, alt-text and an image in the page. Gif-ly works by associating emotions of the gif as a metadata along with the images. 

For a true FTS to work over a bunch of images one way to do is by extracting text from those images using an OCR and using it as the metadata for search

## Handling Misspellings - Fuzzy Search

Fuzzy search is a terminology used in Elasticsearch. It uses Damerau-Levenshtein distance formula. 

The Damerau-Levenshtein distance between two pieces of text is the number of insertions, deletions, substitutions, and transpositions needed to make one string match the other. 

For example, the Levenshtein distance between the words “ax” and “axe” is 1 due to the single deletion required.

## Updating New Data
Indexes are built based on the data in the databases. In any real time system the data changes frequently. For e.g., An item might go out of stock or the prices might vary and so on. In this case the index becomes invalid and searching over it often gives wrong results. This can be handled in 2 ways

1. Drop the index and rebuild it for the newly available data
	- It is time consuming 
	- User can’t do FTS until the whole index is rebuilt again
2. Keep track of all the updates and inserts to the DB and update the index asynchronously
	- The only drawback in this method is the inconsistency in data, which is much better when compared to shutting off the feature for few minutes.

## Full-Text-Search In Distributed Systems
As the system scales and when you adapt to a microservices architecture next set of challenges occurs. 
1. [How to search through the data which is spread across different microservices?](https://slack.engineering/search-at-slack-431f8c80619e)
2. As the data scales a user with less data might get his response faster, when compared to one whose drive is overflowing. [how to efficiently index the documents so that the latency does not vary for different users.](https://blogs.dropbox.com/tech/2015/03/firefly-instant-full-text-search-engine/)
 
## How to get Started?

[Here is a step-by-step walkthrough on how to implemnent an Elastic search powered applicaiton](https://blog.patricktriest.com/text-search-docker-elasticsearch/)

## Resources
1. [https://issart.com/blog/full-text-search-how-it-works/](https://issart.com/blog/full-text-search-how-it-works/)
2. [https://medium.com/dev-channel/how-to-add-full-text-search-to-your-website-4e9c80ce2bf4](https://medium.com/dev-channel/how-to-add-full-text-search-to-your-website-4e9c80ce2bf4)
3. [https://www.youtube.com/watch?v=FM2e2J7OJpM](https://www.youtube.com/watch?v=FM2e2J7OJpM)
4. [How does a Lucene Query work?](https://www.youtube.com/watch?v=Z-yG-KvIuD8)
5. [Do Not Use MySQL indexes](https://hackernoon.com/dont-waste-your-time-with-mysql-full-text-search-61f644a54dfa)
6. [How does FTS work what can it do?](https://www.youtube.com/watch?v=VBc4qammHrY)
7. [https://conferences.xeraa.net/videos/ovUA3r](https://conferences.xeraa.net/videos/ovUA3r)
8. [How dropbox solves full text search](https://blogs.dropbox.com/tech/2015/03/firefly-instant-full-text-search-engine/)