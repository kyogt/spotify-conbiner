import base64
import json
import requests
from urllib.parse import urlparse, parse_qs
import http.server
import socketserver
import webbrowser
import urllib.parse
import os
import sys

# Fill in your Spotify app credentials
CLIENT_ID = "4d54bc8c7d244ea090e787329ad1ffe0"
CLIENT_SECRET = "5a6aa2dc55534855864341e9e598ddbd"
REDIRECT_URI = "http://localhost:8000"
PORT = 8000
AUTH_CODE = None

# Scopes required for the application
SCOPES = "playlist-read-private playlist-modify-public playlist-modify-private"

class TokenHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global AUTH_CODE
        
        query_components = parse_qs(urlparse(self.path).query)
        if 'code' in query_components:
            AUTH_CODE = query_components['code'][0]
            
            # Send a response to the browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_message = """
            <html>
            <body>
                <h1>Authorization Successful!</h1>
                <p>You can now close this window and return to the terminal.</p>
            </body>
            </html>
            """
            
            self.wfile.write(success_message.encode('utf-8'))
            
            # Stop the server after receiving the code
            def shutdown_server():
                httpd.shutdown()
            
            import threading
            threading.Thread(target=shutdown_server).start()
        else:
            # Handle other paths or error
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def get_auth_code():
    global httpd
    
    # Step 1: Redirect user to the Spotify authorization page
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPES,
        'redirect_uri': REDIRECT_URI
    })
    
    print(f"Opening browser to authorize the application...")
    webbrowser.open(auth_url)
    
    # Set up temporary server to capture the redirect with the auth code
    httpd = socketserver.TCPServer(("", PORT), TokenHandler)
    print(f"Waiting for authorization... (listening on port {PORT})")
    
    httpd.serve_forever()
    
    if AUTH_CODE:
        print("Authorization code received!")
        return AUTH_CODE
    else:
        print("Failed to get authorization code.")
        sys.exit(1)

def get_tokens(auth_code):
    # Step 2: Exchange the auth code for access and refresh tokens
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
    
    response = requests.post(token_url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting tokens: {response.text}")
        return None

if __name__ == "__main__":
    # Get the authorization code
    auth_code = get_auth_code()
    
    # Exchange the auth code for tokens
    token_data = get_tokens(auth_code)
    
    if token_data and 'refresh_token' in token_data:
        print("\n===== SUCCESS =====")
        print("Access Token:", token_data['access_token'])
        print("\nRefresh Token:", token_data['refresh_token'])
        print("\nSave the refresh token securely - you'll need it for the GitHub Actions workflow.")
        print("Add it as a secret named SPOTIFY_REFRESH_TOKEN in your GitHub repository.")
        print("Also add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET as secrets.")
    else:
        print("Failed to get tokens.")
