import json
from ChatBotHelper.executeSQLQuery import execute_sql_query
from ChatBotHelper.generateSQLQuery import generate_sql_query

def SQLAgent(state, llm, schemaContext, sqlPromptTemplate,  supabase,memory,formatType = "json"):
    user_input = state["user_input"]
    sql_query = generate_sql_query(user_input, llm, schemaContext, sqlPromptTemplate, memory)
    raw_result = execute_sql_query(sql_query, llm, supabase, formatType)
    # Ensure raw_result is always a string
    # Format the SQL query result if it's a list of dictionaries
    if isinstance(raw_result, list):
        # Convert the list of dictionaries into a readable string (e.g., as JSON or a simple table format)
        formatted_result = "\n".join(
            [json.dumps(item, indent=2) for item in raw_result])  # or customize how you want to format the list
    elif isinstance(raw_result, dict):
        formatted_result = json.dumps(raw_result, indent=2)  # Convert dictionary to readable JSON
    elif isinstance(raw_result, str):
        formatted_result = raw_result.strip()  # Clean up the result if it's a string
    else:
        formatted_result = "The SQL query executed successfully, but no results were returned."
    # print(formatted_result)
    memory.save_context({"input": f"SQL: {sql_query}"}, {"output": formatted_result})
    messages = state.get("messages", [])  # Retrieve existing messages or initialize
    messages.append({"role": "assistant", "content": formatted_result})  # Append latest response
    return {
        "user_input": user_input,
        "messages": messages,  # Ensure messages is updated
    }