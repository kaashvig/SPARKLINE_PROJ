from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("YOUR_API_KEY") or os.getenv("GROQ_API_KEY")

client = None
if api_key:
    client = Groq(api_key=api_key)

def generate_answer(question: str, result: list) -> str:
    result_str = str(result)[:2000] # Limit size to prevent token limits
    
    prompt = f"""
 You are a business intelligence assistant.

 User Question:
 {question}

  SQL Query Execution Result:
  {result_str}

 IMPORTANT RULES:
 - Answer ONLY using information present in the SQL result.
 - Do NOT use outside knowledge.
 - Do NOT guess or assume facts.
 - Do NOT infer information not present in the result.
 - If the result does not contain enough information to answer the question, respond exactly:
 "The requested information is not available in the database."

 Provide a concise professional answer.
"""
    
    if client:
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error using Groq API: {str(e)}. Fallback: Retrieved {len(result)} records. Data: {result_str}"
    else:
        # Structured fallback if API key is not configured
        if not result:
            return "No matching records found in the database."
        return f"Database query returned {len(result)} record(s). Sample result: {result[0]}"
