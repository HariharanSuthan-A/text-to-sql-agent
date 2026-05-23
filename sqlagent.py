
from httpx import request
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()
import os




def text_to_sql(query: str) -> str:
    """Returns a SQL query based on the user's input."""
    return f"Sql query" , {query}



model = ChatGroq(
    model="Llama-3.3-70B-Versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)



text_to_sql_agent = create_agent(
    model=model,
    tools = [text_to_sql],
    system_prompt="""You are a SQL query generator. Convert natural language questions into valid SQLite SQL queries.

Database schema:
- Table: employees
- Columns: id (INTEGER PRIMARY KEY), first_name (TEXT), last_name (TEXT), department (TEXT), salary (REAL), hire_date (TEXT)

Rules:
1. Return ONLY the SQL query - no explanations, no markdown, no "The SQL query is:" prefixes
2. Handle natural language comparisons:
   - "high", "highest", "most" → ORDER BY salary DESC LIMIT 1 or >= threshold
   - "low", "lowest", "least" → ORDER BY salary ASC LIMIT 1 or <= threshold
   - "above", "more than", "greater than" → >
   - "below", "less than", "under" → <
   - "at least", "minimum" → >=
   - "at most", "maximum" → <=
3. For "all records" queries without conditions: SELECT * FROM employees
4. For specific columns: SELECT first_name, last_name, salary FROM employees
5. For aggregations: use AVG(), MAX(), MIN(), COUNT() as needed
6. For departments: WHERE department = 'DepartmentName'
7. For date comparisons: WHERE hire_date > 'YYYY-MM-DD'

Examples:
- "who gets highest salary" → SELECT * FROM employees ORDER BY salary DESC LIMIT 1
- "employees with salary above 90000" → SELECT * FROM employees WHERE salary > 90000
- "lowest paid employee" → SELECT * FROM employees ORDER BY salary ASC LIMIT 1
- "average salary in Engineering" → SELECT AVG(salary) FROM employees WHERE department = 'Engineering'

Output ONLY valid SQL that can be executed directly.""",
)

def run_cli():
    """Run the interactive CLI version"""
    while True:
        query = input("Enter your question (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        else :
            response = text_to_sql_agent.invoke({
        "messages": [{"role":"user","content": query}]
        
    })
            print(f"Here is the SQL Query:",response["messages"][-1].content)

            from sqlite3 import connect

            conn = connect("data/employees.db")   # persistent file
            cursor = conn.cursor()

            cursor.execute(response["messages"][-1].content)
            rows = cursor.fetchall()

            conn.close()
            print("🤖 Here is the retrived data from the table:")
            print("="*60)
            for row in rows:
                print(row)
            print("="*60)

            data = str(rows)


            sql_to_text_agent = create_agent(
                model=model,
                system_prompt="You are a helpful assistant that you convert the retrived data into natural language text.",

            )


            result = sql_to_text_agent.invoke({
                "messages": [{"role":"user","content":data}]
                
            })


            print("⚛",result['messages'][-1].content)

if __name__ == "__main__":
    run_cli()


