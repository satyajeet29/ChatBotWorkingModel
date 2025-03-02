import pandas as pd
def format_results_naturally(result_data):
    """Convert SQL query results into a natural language summary"""
    if not result_data:
        return "Sorry, no matching records were found."

    if isinstance(result_data, dict):  # If Supabase returns a single dictionary
        result_data = [result_data]

    if isinstance(result_data, list) and result_data:
        # Convert to DataFrame for processing
        df = pd.DataFrame(result_data)

        # If there's only one row, display it as a sentence
        if len(df) == 1:
            row = df.iloc[0].to_dict()
            return "Here’s what I found:\n" + "\n".join([f"- {key}: {value}" for key, value in row.items()])

        # For multiple rows, list them as bullet points
        response = "Here are the results:\n"
        for index, row in df.iterrows():
            response += f"\n🔹 Result {index + 1}:\n"
            response += "\n".join([f"  - {key}: {value}" for key, value in row.to_dict().items()])
            response += "\n"

        return response

    return "Unexpected result format."