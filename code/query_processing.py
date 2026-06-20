
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Support both YOUR_API_KEY and GROQ_API_KEY
api_key = os.getenv("GROQ_API_KEY")
def get_client():
    if not api_key:
        raise ValueError("Groq API Key is not configured. Please set YOUR_API_KEY or GROQ_API_KEY in the .env file.")
    return Groq(api_key=api_key)

def generate_sql(question, schema):

    prompt = f"""
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
    """

    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql_query = response.choices[0].message.content.strip()

    return sql_query
