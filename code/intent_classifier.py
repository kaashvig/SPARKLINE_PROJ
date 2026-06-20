from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def classify_intent(question: str):

    
    prompt = f"""
         You are a security classifier.

         Classify the request as:
         READ
         or
         WRITE
         or
         INVALID

          READ:
           - Asking for information
           - Reports
           - Analytics
           - Aggregations

          WRITE:
           - Insert
           - Update
           - Delete
           - Modify
           - Change
           - Increase
           - Decrease
           - Create
           - Remove
           - Any action that changes data

           INVALID:
          - Gibberish
          - Random text
          - Unclear requests
          - Non-business questions

         Return ONLY:
         READ
         or
         WRITE
         or 
         INVALID

         Question:
         {question}
 """



    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip().upper()