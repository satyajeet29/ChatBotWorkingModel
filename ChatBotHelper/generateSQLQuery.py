def generate_sql_query(user_input, llm, schemaContext, sqlPromptTemplate):
    """Convert user input into an SQL query using OpenAI"""
    messages = [
        {"role": "system", "content": schemaContext},
        {"role": "user", "content": sqlPromptTemplate.format(query=user_input)}
    ]
    response = llm.invoke(messages)
    return response.content.replace("```sql", "").replace("```", "").replace(";", "").strip()