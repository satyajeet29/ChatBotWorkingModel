from langchain.chains import LLMChain

def generate_sql_query(user_input, llm, schemaContext, sqlPromptTemplate, memory):
    """Convert user input into an SQL query using OpenAI"""
    chat_history = memory.load_memory_variables({})["history"]

    # ✅ Check if the user is referring to a past query
    if "last query" in user_input.lower() or "previous query" in user_input.lower():
        last_sql_query = None

        #  Extract the last SQL query from history
        for entry in reversed(chat_history):
            if "SELECT" in entry["output"]:  # Rough check for SQL query presence
                last_sql_query = entry["output"]
                break

        if last_sql_query:
            user_input = f"{user_input}\nBased on this previous query: {last_sql_query}"

    messages = [
        {"role": "system", "content": schemaContext},
        {"role": "user", "content": sqlPromptTemplate.format(query=user_input)}
    ]
    response = llm.invoke(messages)
    sql_query = response.content.replace("```sql", "").replace("```", "").replace(";", "").strip()
  
    return sql_query