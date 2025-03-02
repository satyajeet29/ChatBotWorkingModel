import os
from dotenv import load_dotenv
from supabase import create_client, Client
#helper files
from azureOpenAI import azureOpenAI, azureChatOpenAI
from langchain.memory import ConversationBufferMemory
from SupabaseAuth.emailAuth import login_with_email
from PromptEngineering.schemaContext import generateSchemaContext
from PromptEngineering.chatPromptTemplate import sqlPromptTemplate
from Chatbot import chatbot
import warnings
warnings.filterwarnings("ignore")
# Load environment variables from .env file
load_dotenv()
supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
azure_openai = azureOpenAI(os.getenv("AZURE_OPENAI_API_KEY"),"2023-12-01-preview",os.getenv("AZURE_OPENAI_ENDPOINT"))
user = login_with_email(os.environ.get("subapase_email"), os.environ.get("subapase_password"), supabase)
SCHEMA_CONTEXT = generateSchemaContext() # Schema Conextualization
# Define prompt template for SQL generation
SQL_PROMPT_TEMPLATE = sqlPromptTemplate(SCHEMA_CONTEXT)
DEBUG_MODE = False
llm = azureChatOpenAI()

# Initialize memory (stores chat history)
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

if __name__ == "__main__":
    chatbot( supabase,memory,  llm=llm,  schemaContext=SCHEMA_CONTEXT, sqlPromptTemplate=SQL_PROMPT_TEMPLATE, formatType="json",DEBUG_MODE = False)