def classify_query(user_query, llm):
    """Determine if the user query is for SQL generation, executing a query, or a general response."""
    classification_prompt = f"""
    Classify the following user query into one of three categories:
    - "sql_generation": If the query requires generating an SQL statement.
    - "execute_sql": If the query requires running an SQL statement and formatting the result.
    - "general_response": If the query is a general question unrelated to SQL.

    User query: "{user_query}"

    Respond with ONLY the category name.
    """
    classification = llm.invoke(classification_prompt).content.strip().lower()
    return classification