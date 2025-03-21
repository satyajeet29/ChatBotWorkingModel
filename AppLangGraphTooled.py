import os
from dotenv import load_dotenv
from supabase import create_client, Client
#helper files
from azureOpenAI import azureOpenAI, azureChatOpenAI
from SupabaseAuth.emailAuth import login_with_email
from PromptEngineering.schemaContext import generateSchemaContext
from PromptEngineering.chatPromptTemplate import sqlPromptTemplate
from Chatbot import chatbot
import warnings
from langchain.memory import ConversationBufferMemory
from ChatBotGraphTooled import build_chatbot_graph

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
memory = ConversationBufferMemory()
# Build and compile chatbot graph
app = build_chatbot_graph(llm, SCHEMA_CONTEXT, SQL_PROMPT_TEMPLATE, memory, supabase)
print("Supabase Chatbot (type 'exit' to stop)")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Run Graph
    # Check if messages exist before accessing them
    result = app.invoke({"user_input": user_input, "messages": []})  # Ensure messages list is initialized

    if "messages" in result and result["messages"]:
        last_message = result["messages"][-1].get("content", "").strip()
        if last_message:
            print(f"\nGreenAIAssistant: {last_message}")
        else:
            print("\nGreenAIAssistant: The query executed, but no meaningful response was generated.\n")
    else:
        print(result)
        print("\nGreenAIAssistant: No response was generated. Please try again.\n")
