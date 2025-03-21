from ChatBotHelper.generateSQLQuery import generate_sql_query
from ChatBotHelper.SQLAgent import SQLAgent
from langchain.schema import SystemMessage


def decide_and_execute(state, llm, schemaContext, sqlPromptTemplate, memory,supabase,formatType = "json"):
    user_input = state["user_input"]

    # LLM decides the type of query
    system_message = SystemMessage(
        content="Classify if the query requires SQL execution ('sql_generation') or is a general response ('general_response'). Only return 'sql_generation' or 'general_response'.")
    decision = llm.invoke([system_message, user_input]).content.strip()
    memory.save_context({"input": user_input}, {"output": decision})
    #return decision
    return {"query_type": decision if decision in {"sql_generation", "general_response"} else "general_response"}
