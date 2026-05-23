# SQL Agent - Text-to-SQL Conversion System

A conversational SQL agent that converts natural language questions into SQL queries, executes them against a SQLite database, and converts results back to natural language responses.

## 🎯 Overview

The SQL Agent is a LLM-powered system that bridges the gap between natural language and database queries. Users can ask questions in plain English, and the system automatically generates and executes the appropriate SQL queries, returning results in conversational format.

**Tech Stack:**
- LLM: Groq (Llama 3.3-70B-Versatile)
- Framework: LangChain
- Database: SQLite
- Language: Python

---

## 🔄 How It Works

### Step-by-Step Process

1. **User Input** → User asks a question in natural language (e.g., "Who has the highest salary?")
2. **Text-to-SQL Agent** → LLM converts the natural language query to valid SQL
3. **SQL Execution** → Query runs against the SQLite database (employees table)
4. **Data Retrieval** → Raw results are fetched from the database
5. **SQL-to-Text Agent** → LLM converts the raw data back into readable natural language
6. **Response** → User receives a formatted answer

### Database Schema

```
Table: employees
├── id (INTEGER PRIMARY KEY)
├── first_name (TEXT)
├── last_name (TEXT)
├── department (TEXT)
├── salary (REAL)
└── hire_date (TEXT)
```

---

## 📊 Architecture Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌──────────────────┐        ┌──────────────────┐         │
│  │   User Query     │        │  Example: "Who   │         │
│  │  (Natural Lang)  │────▶   │  gets highest    │         │
│  │                  │        │  salary?"        │         │
│  └──────────────────┘        └──────────────────┘         │
│           │                                                │
│           ▼                                                │
│  ┌──────────────────────────────────────┐                 │
│  │   Text-to-SQL Agent (LLM)            │                 │
│  │   - Groq Llama 3.3-70B               │                 │
│  │   - Processes natural language       │                 │
│  │   - Generates SQL query              │                 │
│  └──────────────────────────────────────┘                 │
│           │                                                │
│           ▼                                                │
│  ┌──────────────────────────────────────┐                 │
│  │  Generated SQL Query                 │                 │
│  │  SELECT * FROM employees             │                 │
│  │  ORDER BY salary DESC LIMIT 1        │                 │
│  └──────────────────────────────────────┘                 │
│           │                                                │
│           ▼                                                │
│  ┌──────────────────────────────────────┐                 │
│  │  SQLite Database                     │                 │
│  │  (employees.db)                      │                 │
│  └──────────────────────────────────────┘                 │
│           │                                                │
│           ▼                                                │
│  ┌──────────────────────────────────────┐                 │
│  │  Raw Query Results                   │                 │
│  │  [(1, 'John', 'Doe', 'Eng', 120000)] │                 │
│  └──────────────────────────────────────┘                 │
│           │                                                │
│           ▼                                                │
│  ┌──────────────────────────────────────┐                 │
│  │  SQL-to-Text Agent (LLM)             │                 │
│  │  - Converts data to natural language │                 │
│  │  - Formats response                  │                 │
│  └──────────────────────────────────────┘                 │
│           │                                                │
│           ▼                                                │
│  ┌──────────────────────────────────────┐                 │
│  │  Natural Language Response           │                 │
│  │  "John Doe from Engineering has the  │                 │
│  │   highest salary at $120,000"        │                 │
│  └──────────────────────────────────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Query Translation Examples

The agent intelligently handles various natural language patterns:

| Natural Language | Generated SQL |
|---|---|
| "Who has the highest salary?" | `SELECT * FROM employees ORDER BY salary DESC LIMIT 1` |
| "Show employees earning above 90000" | `SELECT * FROM employees WHERE salary > 90000` |
| "Average salary in Engineering" | `SELECT AVG(salary) FROM employees WHERE department = 'Engineering'` |
| "List all employees" | `SELECT * FROM employees` |
| "Employees hired after 2022" | `SELECT * FROM employees WHERE hire_date > '2022-01-01'` |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Installation

1. **Install dependencies:**
   ```bash
   pip install langchain langchain-groq python-dotenv sqlite3
   ```

2. **Create a `.env` file:**
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

3. **Initialize the database** (run `db-creation.ipynb` notebook)

### Project Structure
```
sqlagent/
├── sqlagent.py          # Main agent code
├── db-creation.ipynb    # Database initialization
├── data/
│   └── employees.db     # SQLite database
└── README.md           # This file
```

---

## 💻 Usage

Run the interactive CLI:

```bash
python sqlagent.py
```

Then type your questions:
```
Enter your question (or 'exit' to quit): Who gets the highest salary?
🤖 Here is the SQL Query: SELECT * FROM employees ORDER BY salary DESC LIMIT 1
...
⚛ John Doe has the highest salary at $120,000 in the Engineering department.
```

---

## 🔧 Key Components

### 1. **Text-to-SQL Agent**
- Powered by Groq's Llama 3.3-70B model
- Converts natural language to SQL queries
- Understands comparisons: "highest" → ORDER BY DESC, "above" → >
- Handles aggregations, departments, and date filters

### 2. **SQL Executor**
- Connects to SQLite database
- Safely executes generated queries
- Returns structured results

### 3. **SQL-to-Text Agent**
- Converts raw query results into natural language
- Formats responses for readability
- Provides context about the data retrieved

---

## 📝 Notes

- The system currently supports the `employees` table with predefined schema
- Queries are executed directly without additional validation
- All responses are generated using LLM - may have minor variations in wording

---

## 🔗 Links

- [LangChain Documentation](https://python.langchain.com/)
- [Groq API](https://console.groq.com/)
- [SQLite Documentation](https://www.sqlite.org/)
