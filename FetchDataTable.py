# Not sure if it is needed
def fetch_data_from_table(table_name):
    try:
        # Query the table and fetch the data
        data = supabase.table(table_name).select("*").execute()

        # Check if the data is retrieved successfully
        if data.data:
            print(f"Data from '{table_name}':")
            for row in data.data:
                print(row)
        else:
            print(f"No data found in table '{table_name}'.")

    except Exception as e:
        print(f"Error fetching data from '{table_name}': {e}")