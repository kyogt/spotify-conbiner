import base64
import urllib.parse
import requests
import sys

# Your Spotify app credentials
CLIENT_ID = "4d54bc8c7d244ea090e787329ad1ffe0"
CLIENT_SECRET = "5a6aa2dc55534855864341e9e598ddbd"
REDIRECT_URI = "http://localhost:8000"

# Required scopes
SCOPES = "playlist-read-private playlist-modify-public playlist-modify-private"

def step1_get_auth_url():
    """Generate the authorization URL"""
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPES,
        'redirect_uri': REDIRECT_URI
    })
    
    print("\n=== STEP 1: AUTHORIZATION ===")
    print("1. Copy this URL and open it in your browser:")
    print(f"\n{auth_url}\n")
    print("2. Log in to Spotify if prompted and authorize the app")
    print("3. After authorizing, you'll be redirected to a URL that looks like:")
    print("   http://localhost:8000?code=LONG_CODE_HERE")
    print("4. Copy the entire 'code' parameter value for the next step")

def step2_get_refresh_token():
    """Exchange authorization code for tokens"""
    print("\n=== STEP 2: GET REFRESH TOKEN ===")
    auth_code = input("Enter the authorization code from the URL: ")
    
    token_url = "https://accounts.spotify.com/api/token"
    
    # Create Basic Authorization header
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    print("Requesting tokens...")
    response = requests.post(token_url, headers=headers, data=payload)
    
    if response.status_code == 200:
        token_data = response.json()
        print("\n=== SUCCESS! ===")
        print("Here's your refresh token (save this somewhere secure):")
        print("\nRefresh Token:", token_data['refresh_token'])
        print("\nAdd this as SPOTIFY_REFRESH_TOKEN in your GitHub repository secrets")
        print("along with SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET")
    else:
        print(f"Error getting tokens: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("Spotify Authorization Helper")
    print("This script will help you get a refresh token for your Spotify API access")
    
    while True:
        print("\nOptions:")
        print("1. Generate authorization URL")
        print("2. Exchange authorization code for refresh token")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1, 2, or 3): ")
        
        if choice == "1":
            step1_get_auth_url()
        elif choice == "2":
            step2_get_refresh_token()
        elif choice == "3":
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
