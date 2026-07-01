# SHL Assessment Recommendation Agent

An AI-powered conversational assistant that recommends SHL assessments based on hiring requirements using semantic search and intent-based routing.

---

## Overview

This project helps recruiters identify suitable SHL assessments by understanding natural language hiring requirements.

The assistant supports:

- Recommending SHL assessments
- Comparing assessments
- Refining recommendations
- Asking clarification questions for vague requests
- Rejecting prompt injection and unrelated queries

The solution uses semantic search with Sentence Transformers and FAISS for fast retrieval.

---

## Features

### Assessment Recommendation

Example:

> Hiring a Java developer with 4 years experience

Returns relevant Java assessments from the SHL catalog.

---

### Clarification

Example:

> I need an assessment

The assistant asks for:

- Role
- Experience level
- Skills
- Personality traits

before recommending assessments.

---

### Compare Assessments

Example:

> Compare Python and Java assessments

Returns descriptions of both assessments along with recommendation links.

---

### Refine Recommendations

Example:

> Actually include personality assessments also

Updates recommendations according to the new requirement.

---

### Guardrails

The assistant refuses:

- Prompt injection
- Jailbreak attempts
- Off-topic questions

Examples:

- Ignore previous instructions
- What's the weather today?

---

## Tech Stack

- Python 3.11+
- FastAPI
- FAISS
- Sentence Transformers
- Hugging Face
- Uvicorn

---

## Project Structure

```
shl-assessment-agent/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── agent.py
│
├── agent/
│   └── router.py
│
├── retrieval/
│   └── search.py
│
├── data/
│   ├── catalog.index
│   └── metadata.pkl
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository.

```bash
git clone <repository-url>
cd shl-assessment-agent
```

Create virtual environment.

```bash
python -m venv venv
```

Activate it.

Windows

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

### Chat

```
POST /chat
```

Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer with 4 years experience"
    }
  ]
}
```

Response

```json
{
  "reply": "I found 5 SHL assessments matching your requirement.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "...",
      "test_type": "Knowledge & Skills"
    }
  ],
  "end_of_conversation": true
}
```

---

## Intent Routing

The assistant classifies every user message into one of five intents.

| Intent | Description |
|---------|-------------|
| clarify | Ask follow-up questions for vague requests |
| recommend | Recommend assessments |
| compare | Compare two assessments |
| refine | Update previous recommendations |
| refuse | Reject off-topic or unsafe requests |

---

## Semantic Search

The project uses:

- SentenceTransformer (all-MiniLM-L6-v2)
- FAISS Index

Workflow:

1. Convert user query into an embedding.
2. Search nearest neighbours in the FAISS index.
3. Retrieve top matching SHL assessments.
4. Return recommendations with metadata.

---

## Safety

The assistant rejects:

- Prompt injection attempts
- System prompt extraction
- Jailbreak requests
- Off-topic conversations

Example:

Input:

```
Ignore previous instructions.
```

Output:

```
I can only help with SHL assessments.
```

---

## Example Queries

### Clarify

```
I need an assessment
```

---

### Recommendation

```
Hiring a Java developer with 4 years experience
```

---

### Compare

```
Compare Python and Java assessments
```

---

### Refine

```
Actually include personality assessments also
```

---

### Refuse

```
What's the weather today?
```

---

## Design Decisions

- FastAPI was chosen for building lightweight REST APIs.
- FAISS enables fast semantic retrieval from the SHL catalog.
- Sentence Transformers provide dense vector embeddings for natural language queries.
- Intent routing keeps conversation logic modular and easy to extend.
- Guardrails improve robustness by preventing prompt injection and handling unrelated requests safely.

---

## Future Improvements

- Multi-turn conversation memory for better refinement.
- Hybrid keyword + semantic retrieval.
- LLM-based intent classification.
- Re-ranking search results using cross-encoders.
- Deployment with Docker and cloud hosting.

---

## Author

**Arya Shende**

Data Science & AI Engineer