def genericResponse(user_query, llm):
    """Use LLM to generate a generic response for user queries that don't require SQL."""
    prompt = f"""You are an intelligent assistant for green building management. Please answer the following user query in a clear and concise manner:
    
    User query: "{user_query}"
    
    Provide a well-structured response."""

    response = llm.invoke(prompt).content.strip()
    return response