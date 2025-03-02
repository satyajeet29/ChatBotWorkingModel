from ChatBotHelper.executeSQLQuery import execute_sql_query
from ChatBotHelper.generateSQLQuery import generate_sql_query
from ChatBotHelper.QueryClassifier import classify_query
from ChatBotHelper.GeneralResponse import genericResponse
def chatbot(supabase, memory, llm, schemaContext, sqlPromptTemplate, formatType = "markdown", DEBUG_MODE = False):
    """Main chatbot loop"""
    print("Supabase Chatbot (type 'exit' to stop)")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        queryType = classify_query(user_input, llm)
        if queryType == "sql_generation":
            sql_query = generate_sql_query(user_input, llm, schemaContext, sqlPromptTemplate)
            result = execute_sql_query(sql_query, llm, supabase, formatType)
            print(f"\n{result}\n")
        elif queryType == "general_response":
            result = genericResponse(user_input, llm, memory)
            print(f"\n{result}\n")


        if DEBUG_MODE:
            if queryType == "sql_generation":
                print(f"\nGenerated SQL:\n{sql_query}\n")  # Only show if debugging