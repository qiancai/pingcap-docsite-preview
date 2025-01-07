---
title: AI Features
summary: Learn about AI features for TiDB Cloud.
---

# AI Features

The AI features in TiDB Cloud enable you to fully leverage advanced technologies for data exploration, search, and integration. From natural language-driven SQL query generation to high-performance vector search, TiDB combines database capabilities with modern AI features to power innovative applications. With support for popular AI frameworks, embedding models, and seamless integration with ORM libraries, TiDB offers a versatile platform for use cases such as semantic search and AI-powered analytics.

This document highlights these AI features and how they enhance the TiDB experience.

## Chat2Query

Chat2Query is an AI-powered feature integrated into SQL Editor that assists users in generating, debugging, or rewriting SQL queries using natural language instructions. For more information, see [Explore your data with AI-assisted SQL Editor](/tidb-cloud/explore-data-with-chat2query.md).

In addition, TiDB Cloud provides a Chat2Query API for TiDB Cloud Serverless clusters. After it is enabled, TiDB Cloud will automatically create a system Data App called Chat2Query and a Chat2Data endpoint in Data Service. You can call this endpoint to let AI generate and execute SQL statements by providing instructions. For more information, see [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md).

## Vector Search

Vector search is a search method that prioritizes the meaning of your data to deliver relevant results.

Unlike traditional full-text search, which relies on exact keyword matching and word frequency, vector search converts various data types (such as text, images, or audio) into high-dimensional vectors and queries based on the similarity between these vectors. This search method captures the semantic meaning and contextual information of the data, leading to a more precise understanding of user intent.

Even when the search terms do not exactly match the content in the database, vector search can still provide results that align with the user's intent by analyzing the semantics of the data. For example, a full-text search for "a swimming animal" only returns results containing these exact keywords. In contrast, vector search can return results for other swimming animals, such as fish or ducks, even if these results do not contain the exact keywords.

For more information, see [Vector Search (Beta) Overview](/tidb-cloud/vector-search-overview.md).

## AI integrations

### AI frameworks

TiDB provides official support for several popular AI frameworks, enabling you to easily integrate AI applications developed based on these frameworks with TiDB Vector Search.

For a list of supported AI frameworks, see [Vector Search Integration Overview](/tidb-cloud/vector-search-integration-overview.md#ai-frameworks).

### Embedding models and services

A vector embedding, also known as an embedding, is a sequence of numbers that represents real-world objects in a high-dimensional space. It captures the meaning and context of unstructured data, such as documents, images, audio, and videos.

Embedding models are algorithms that transform data into [vector embeddings](/tidb-cloud/vector-search-overview.md#vector-embedding). The choice of an appropriate embedding model is crucial for ensuring the accuracy and relevance of semantic search results.

TiDB Vector Search supports storing vectors of up to 16383 dimensions, which accommodates most embedding models. For unstructured text data, you can find top-performing text embedding models on the [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard).

### Object Relational Mapping (ORM) libraries

Object Relational Mapping (ORM) libraries are tools that facilitate the interaction between applications and relational databases by allowing developers to work with database records as if they were objects in their programming language of choice.

TiDB lets you integrate vector search with ORM libraries to manage vector data alongside traditional relational data. This integration is particularly useful for applications that need to store and query vector embeddings generated by AI models. By using ORM libraries, developers can seamlessly interact with vector data stored in TiDB, leveraging the database's capabilities to perform complex vector operations like nearest neighbor search.

For a list of supported ORM libraries, see [Vector Search Integration Overview](/tidb-cloud/vector-search-integration-overview.md#object-relational-mapping-orm-libraries).