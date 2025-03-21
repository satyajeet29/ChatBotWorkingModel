import json
import os
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from supabase import create_client, Client
from ChatBotHelper.executeSQLQuery import execute_sql_query
from ChatBotHelper.generateSQLQuery import generate_sql_query
from PromptEngineering.chatPromptTemplate import sqlPromptTemplate
from PromptEngineering.schemaContext import generateSchemaContext
from SupabaseAuth.emailAuth import login_with_email

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()
# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register API Routes
# app.include_router(router)

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_key=AZURE_OPENAI_API_KEY
)

prev_user_id = None
SCHEMA_CONTEXT = None
SQL_PROMPT_TEMPLATE = None
supabase = None

class ChatRequest(BaseModel):
    message: str
    user_id: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Supabase AI Chatbot API!"}
@app.post("/query/")
async def query_database(request: ChatRequest):
    """API endpoint for generating and executing SQL queries"""
    print(f"From user {request.user_id}, User Input: {request.message}")  # Debugging

    try:
        # Generate SQL query
        # sql_query = generate_sql_query(request.message)

        SCHEMA_CONTEXT, SQL_PROMPT_TEMPLATE, supabase = init(request.user_id)
        sql_query = generate_sql_query(request.message, llm, SCHEMA_CONTEXT, SQL_PROMPT_TEMPLATE)
        #user = login_with_email(os.environ.get("subapase_email"), os.environ.get("subapase_password"), supabase)

        print(f"Generated SQL Query: {sql_query}")  # Debugging

        # Execute the SQL query
        # result = execute_sql_query(sql_query)
        result, json_formatted, str_formatted = execute_sql_query(sql_query, llm, supabase)
        print(f"SQL Execution Result: {result} \n {json_formatted} \n  {str_formatted}")  # Debugging
        #print(f"Result: {json.dumps(result, indent=2)}\n")
        return {"query": sql_query, "result": result, "json_result": json_formatted, "summary":str_formatted}
    except Exception as e:
        print(f"Caught in query {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/")
async def get_users():
    """Fetches a list of users (name, email, user_id) from Supabase"""
    try:

        response = (supabase.from_("users")
                    .select("user_id, first_name, last_name, email")
                    .order("first_name")
                    .execute())
        print(f" here Fetching users {response}")
        if response.data:
            return response.data
        return []
    except Exception as e:
        return {"error": str(e)}


# ✅ Run FastAPI Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)