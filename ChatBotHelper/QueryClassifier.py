from langchain.schema import SystemMessage, HumanMessage

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

def classifyQuerySystem(user_query, llm):
    """
        Uses an LLM to classify user input as either:
        - 'sql_generation' (for queries requiring database execution)
        - 'general_response' (for non-SQL chatbot replies)

        Parameters:
        - user_input (str): The user's input query.
        - llm (azureChatOpenAI or ChatOpenAI): The language model for classification.

        Returns:
        - str: Either 'sql_generation' or 'general_response'
        """
    system_message = SystemMessage(content="Classify if the query requires SQL execution ('sql_generation') "
                                           "or is a general response ('general_response'). "
                                           "Only return 'sql_generation' or 'general_response'. No extra text.")

    classification = llm.invoke([system_message, HumanMessage(content=user_query)]).content.strip().lower()

    # Ensure classification is valid
    if classification not in {"sql_generation", "general_response"}:
        classification = "general_response"  # Default to general response if unclear

    return classification