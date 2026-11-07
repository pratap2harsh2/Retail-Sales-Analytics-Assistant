# 📊 Retail Sales Analytics Assistant

An AI-powered Retail Analytics Assistant that converts natural language business questions into SQL queries, retrieves relevant database context using Retrieval-Augmented Generation (RAG), executes queries on a retail sales database, and generates business-friendly insights.

## 🚀 Live Demo

Streamlit App: [Add Your Streamlit URL Here]

---

## 📌 Overview

Retail businesses generate massive amounts of transactional data, but extracting insights often requires SQL knowledge. This application allows users to ask questions in plain English and receive accurate answers powered by AI.

Example Questions:

- Which region generated the highest revenue?
- What are the top 5 products by sales?
- Show revenue by category.
- Which customer generated the highest revenue?
- Compare revenue across regions.

The application automatically:

1. Understands the user's question.
2. Retrieves relevant database metadata using Qdrant Vector Search.
3. Generates SQL using Cohere LLM.
4. Validates and executes the SQL query.
5. Returns query results and AI-generated business insights.

---

## 🏗️ System Architecture

```text
User Question
       │
       ▼
Streamlit UI
       │
       ▼
Qdrant Vector Search
       │
       ▼
Metadata Context Retrieval
       │
       ▼
Cohere LLM
       │
       ▼
SQL Query Generation
       │
       ▼
SQL Validation
       │
       ▼
SQLite Database
       │
       ▼
Query Results
       │
       ▼
Business Insights
```

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### LLM & Embeddings
- Cohere Command Model
- Cohere Embeddings

### Vector Database
- Qdrant

### Database
- SQLite

### Data Processing
- Pandas
- OpenPyXL

### Backend
- Python

---

## 📂 Project Structure

```text
Retail-Sales-Analytics-Assistant/
│
├── data/
│   └── Retail_Sales_Text2SQL_MVP.xlsx
│
├── database/
│   └── retail.db
│
├── frontend/
│   └── app.py
│
├── llm/
│   ├── cohere_client.py
│   ├── retrieve_context.py
│   ├── generate_sql.py
│   └── generate_answer.py
│
├── services/
│   ├── sql_validator.py
│   └── sql_executor.py
│
├── vector_store/
│   ├── build_vector_db.py
│   └── qdrant_manager.py
│
├── qdrant_db/
│
├── requirements.txt
│
└── README.md
```

---

## ✨ Features

- Natural Language to SQL
- Retrieval-Augmented Generation (RAG)
- AI-Powered Analytics
- Qdrant Vector Search
- SQL Validation Layer
- Interactive Streamlit Dashboard
- Retail Sales Analysis
- Cloud Deployment Ready

---

## 📊 Sample Questions

### Revenue Analysis

- Which region generated the highest revenue?
- Show revenue by region.
- What is the total revenue?
- Which store generated the highest revenue?
- What is the monthly revenue trend?

### Product Analysis

- Top 5 products by revenue.
- Which product sold the most units?
- Which category generated the highest revenue?
- What are the least-selling products?

### Customer Analysis

- Who are the top customers by revenue?
- Which customer segment contributes the most revenue?
- Show customer-wise revenue.

### Store Analysis

- Which store performs best?
- Compare store-wise revenue.
- Which store has the highest average order value?

### Advanced Analytics

- Compare sales between North and South regions.
- Which products drive the highest revenue?
- What percentage of revenue comes from each category?
- Show the top-performing store in each region.

### Business Questions

- Why does South region have more sales than West region?
- What products drive revenue growth?
- Which category contributes most to overall performance?
- What factors explain revenue differences across regions?

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/retail-sales-analytics-assistant.git

cd retail-sales-analytics-assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment Variables

Create a `.env` file:

```env
COHERE_API_KEY=your_cohere_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run frontend/app.py
```

---

## 📈 Example Workflow

```text
Question:
Which region generated the highest revenue?

↓

Context retrieved from Qdrant

↓

SQL generated using Cohere

↓

SQL validated

↓

SQL executed on SQLite

↓

Results returned

↓

Business insights generated
```

---

## 🔥 Challenges Solved

During development and deployment the following challenges were successfully addressed:

- Streamlit Cloud Deployment
- Cohere API Integration
- Retrieval-Augmented Generation (RAG)
- Qdrant Collection Management
- Qdrant Client Locking Issues
- Qdrant Vector Store Initialization
- Streamlit Secrets Configuration
- Cohere API Rate Limiting
- SQLite Query Execution
- Dynamic SQL Generation

---

## 🎯 Future Improvements

- Multi-Turn Conversation Memory
- Predictive Sales Forecasting
- Automated Dashboard Generation
- Advanced Diagnostic Analytics
- Support for Multiple Databases
- User Authentication
- Download Reports as PDF/Excel
- Interactive Visualizations

---

