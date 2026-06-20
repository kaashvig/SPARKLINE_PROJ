from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from auth import verify_api_key
from user_query import QuestionRequest

from schema_validator import validate_schema_relevance
from schema_extractor import get_schema
from query_processing import generate_sql
from validator import validate_sql
from database import execute_query
from table_extractor import extract_tables
from answer_generator import generate_answer
from intent_classifier import classify_intent
from fastapi import Request
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="Sparkline NL2SQL API",
    description="Natural Language to SQL Query Service",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid request format",
            "details": str(exc)
        }
    )

@app.post("/ask")
async def ask_question(
    request: QuestionRequest,
    _: str = Depends(verify_api_key)
):

    try:

        
        # Validate Question
        

        question = request.question.strip()

        if not question:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Question cannot be empty"
                }
            )

        
        # Step 1: Intent Classification
        

        intent = classify_intent(question)

       

        if intent == "INVALID":
           return JSONResponse(
             status_code=400,
             content={
             "question": question,
             "error": (
                "Unable to understand the question. "
                "Please provide a valid business query."
            )
        }
    )

        if intent == "WRITE":
            return JSONResponse(
                status_code=400,
                content={
                    "question": question,
                    "error": (
                        "Only read-only business questions are supported."
                        
                    )
                }
            )

        
        # Step 2: Extract Schema
        

        schema = get_schema()

        
        # Step 3: Generate SQL
        

        sql_query = generate_sql(
            question,
            schema
        )

        
        # Step 4: Validate SQL
       

        validate_sql(sql_query)

        
        # Step 5: Execute Query
        

        result = execute_query(sql_query)

        
        # Step 6: Extract Tables Used

        tables_used = extract_tables(
            sql_query
        )

        if not validate_schema_relevance(tables_used):

            return JSONResponse(
                status_code=400,
                content={
                    "question": question,
                    "error":
                    "The question does not relate to the available database schema."
                }
            )

        
        # Reject queries that do not reference actual schema tables

        if len(tables_used) == 0:
            return JSONResponse(
                status_code=400,
                content={
                    "question": question,
                    "error": (
                        "The question does not appear to relate "
                        "to the available database schema."
                    )
                }
            )

        # Step 7: Generate Answer

        answer = generate_answer(
            question,
            result
        )
        
        # Step 8: Return Response

        return {
            "question": question,
            "intent": intent,
            "sql": sql_query,
            "tables_used": tables_used,
            "result": result,
            "answer": answer
        }

    except ValueError as e:

        return JSONResponse(
            status_code=400,
            content={
                "error": str(e)
            }
        )

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": "Unable to process request",
                "details": str(e)
            }
        )
