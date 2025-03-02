# Function to sign in using email and password
def login_with_email(email, password, supabaseClient):
    try:
        # Authenticate using email and password
        user = supabaseClient.auth.sign_in_with_password({ "email": email, "password": password })

        if user:
            print("Logged in successfully!")
            #print(f"User: {user}")
            #return user
        else:
            print("Login failed, no user returned.")

    except Exception as e:
        print(f"Error: {e}")