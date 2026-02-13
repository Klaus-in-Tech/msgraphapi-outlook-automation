import msal
import webbrowser
import os
from dotenv import load_dotenv

MS_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

def get_access_token(application_id, client_secret, scopes):
    load_dotenv()
    app = msal.ConfidentialClientApplication(
        application_id, authority="https://login.microsoftonline.com/common", client_credential=client_secret
    )
    
    # Check for refresh token (persists across runs)
    try:
        with open("refresh_token.txt", "r") as f:
            refresh_token = f.read()
        result = app.acquire_token_silent(scopes, account=None, refresh_token=refresh_token)
        print(result+refresh_token)
    except:
        # Authorization code flow if no refresh token
        auth_url = app.get_authorization_request_url(scopes, redirect_uri="http://localhost:8000")
        webbrowser.open(auth_url)
        auth_code = input("Enter the authorization code from the browser: ")
        result = app.acquire_token_by_authorization_code(auth_code, scopes, redirect_uri="http://localhost:8000")
        print(result)
    
    if "access_token" in result:
        # Save refresh token for future use
        with open("refresh_token.txt", "w") as f:
            f.write(result["refresh_token"])
        return {"Authorization": f"Bearer {result['access_token']}", "Content-Type": "application/json"}
    raise Exception("Authentication failed")

if __name__ == "__main__":
    load_dotenv()
    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scopes = ["https://graph.microsoft.com/Mail.ReadWrite","https://graph.microsoft.com/Mail.Send"]
    headers = get_access_token(application_id, client_secret, scopes)
    print(headers)
