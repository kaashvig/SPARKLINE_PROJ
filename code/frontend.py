import streamlit as st
import requests

# Configuration
API_URL = "http://127.0.0.1:8000/ask"

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
st.set_page_config(
    page_title="NL to SQL Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Natural Language to SQL Assistant")

st.write(
    "Ask business questions in plain English and get answers from the database."
)

question = st.text_area(
    "Enter your question",
    placeholder="Example: Who are the top 5 customers by revenue?"
)

if st.button("Ask Question"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:

        with st.spinner("Processing..."):

            try:

                response = requests.post(
                    API_URL,
                    headers={
                        "x-api-key": API_KEY
                    },
                    json={
                        "question": question
                    },
                    timeout=60
                )

                data = response.json()

                if response.status_code != 200:
                    st.error(data.get("error", "Unknown error"))
                else:

                    st.success("Query Executed Successfully")

                    st.subheader("Generated SQL")
                    st.code(
                        data["sql"],
                        language="sql"
                    )

                    st.subheader("Tables Used")
                    st.write(
                        ", ".join(
                            data["tables_used"]
                        )
                    )

                    st.subheader("Business Answer")
                    st.info(
                        data["answer"]
                    )

                    st.subheader("Query Results")

                    if data["result"]:
                        st.dataframe(
                            data["result"],
                            use_container_width=True
                        )
                    else:
                        st.warning(
                            "No records found."
                        )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )