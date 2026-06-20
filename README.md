# Sparkline NL2SQL Assignment

## Overview

This project implements a Natural Language to SQL (NL2SQL) API using FastAPI, SQLite, and Groq LLM.

Users can ask business questions in natural language, and the system:

1. Classifies the request as READ, WRITE, or INVALID.
2. Generates a SQL query using an LLM.
3. Validates the generated SQL.
4. Executes the query on the provided SQLite database.
5. Returns:

   * Generated SQL
   * Tables used
   * Query result
   * Natural language answer

The system only supports read-only database operations.

---

# Project Structure

LLM_Kaashvi_Gupta/

├── README.md

├── requirements.txt

├── sparkline_demo.db

└── code/



---

# Setup & Usage

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure Environment Variables

Create a `.env` file inside the `code` folder:

```env
GROQ_API_KEY=your_groq_api_key
API_KEY=sparkline_secret_key_12345
```

## 3. Start the API

```bash
cd code

uvicorn app:app --reload
```

API will run at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Authentication

The API requires an API key.

Header:

```http
x-api-key: sparkline_secret_key_12345
```

---

# Example API Request

```json
{
  "question": "Show all customers"
}
```

---

# Sample Runs

## 1. Normal Question

Request:

```json
{
  "question": "Show all customers"
}
```

Response:

```json
{
  "question": "Show all customers",
  "intent": "READ",
  "sql": "SELECT * FROM customers",
  "tables_used": ["customers"]
}
```

---

## 2. Aggregation Question

Request:

```json
{
  "question": "Who are the top 5 customers by revenue?"
}
```

Response:

```json
{
  "question": "Who are the top 5 customers by revenue?",
  "intent": "READ",
  "sql": "SELECT c.name, SUM(s.amount) AS revenue FROM customers c JOIN sales s ON c.id=s.customer_id GROUP BY c.name ORDER BY revenue DESC LIMIT 5",
  "tables_used": ["customers", "sales"]
}
```

---

## 3. Refused Request

Request:

```json
{
  "question": "Delete customer data"
}
```

Response:

```json
{
  "question": "Delete customer data",
  "error": "Only read-only business questions are supported."
}
```

---

# Design Decisions

## Architecture

Request Flow:

```text
User Question
      ↓
Intent Classification
      ↓
Schema Extraction
      ↓
SQL Generation
      ↓
SQL Validation
      ↓
Database Execution
      ↓
Table Extraction
      ↓
Answer Generation
      ↓
Response
```

## LLM Choice

Groq was used with:

```text
llama-3.3-70b-versatile
```

Reason:

* Fast inference
* Good SQL generation capability
* Free developer access

## Validation Strategy

Multiple validation layers were implemented:

1. Intent Classification

   * READ
   * WRITE
   * INVALID

2. SQL Validation

   * Only SELECT statements allowed
   * Blocks INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE
   * Prevents multiple SQL statements

3. Schema Validation

   * Queries must reference valid schema tables

## Authentication

FastAPI dependency-based API key validation using:

```http
x-api-key
```

header.

---

# Prompt Design

SQL Generation Prompt:

```text
You are a SQL expert.

Database Schema:
{schema}

Generate ONLY a SQLite SELECT query.

Rules:
- Only generate SELECT statements.
- No explanations.
- No markdown.
- Return SQL only.

Question:
{question}
```

Reasoning:

* Restricts the model to SQL generation only.
* Reduces hallucinations.
* Keeps output predictable and easy to validate.

---

# Assumptions

* Database schema remains unchanged.
* Users only require read-only access.
* LLM output may be imperfect and therefore must be validated before execution.
* SQLite is the target database engine.

---

# Limitations & Future Improvements

Current Limitations:

* Intent classification relies on an LLM.
* Some schema-relevant but semantically incorrect questions may still generate valid SQL.
* SQL generation quality depends on the LLM.

Future Improvements:

* Schema-aware semantic validation.
* Column-level validation.
* Query caching.
* Conversation memory.
* Support for additional database engines.

---

# Tools & Resources Used

* FastAPI
* SQLite
* Groq API
* Python
* Swagger UI

Rejected Approach:

A simple keyword-based filter was initially considered for detecting write operations.

Example:

```text
delete
update
insert
drop
```

This approach was rejected because it can miss semantically equivalent requests.

An LLM-based intent classification layer was implemented instead.

---

# SUMMARY

Implemented using FastAPI, SQLite, and Groq Llama 3.3 70B Versatile with a layered validation approach for secure NL2SQL generation.
