from ChatBotHelper.formatResults import format_results_naturally
import json
def execute_sql_query(sql_query, llm,supabase, formatType):
    """Execute the generated SQL query on Supabase and return formatted results"""
    try:
        response = supabase.rpc("run_sql", {"query": sql_query}).execute()
        result_data = response.data

        #return format_results_naturally(result_data)
        # Use LLM to format the JSON into a Markdown table
        format_prompt = f"""
               Convert the following JSON data into a Markdown table. Do not wrap the output in a code block.

               {json.dumps(result_data)}

               Ensure the table is well-formatted and readable.
               """
        if formatType == "markdown":
            markdown_table = llm.invoke(format_prompt)
            return markdown_table.content
        elif formatType == "json":
            return json.dumps(result_data)

    except Exception as e:
        return f"Error executing query: {e}"