import os
import base64
import json
import requests
from datetime import datetime
from urllib.parse import urlencode

# Spotify credentials
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('SPOTIFY_REFRESH_TOKEN')

# Playlist IDs
DISCOVER_WEEKLY_ID = '37i9dQZEVXcORVfIiGFFRu'
RELEASE_RADAR_ID = '37i9dQZEVXbqUM8qIcjHjF'
COMBINED_PLAYLIST_ID = '6SJohidvTEKU0Q6L6gockF'

# Spotify API endpoints
TOKEN_URL = 'https://accounts.spotify.com/api/token'
PLAYLIST_ENDPOINT = 'https://api.spotify.com/v1/playlists/'
USER_ENDPOINT = 'https://api.spotify.com/v1/me'

def get_access_token():
    """Get Spotify access token using refresh token."""
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }
    
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    if response.status_code != 200:
        print(f"Error getting token: {response.text}")
        return None
    
    return response.json()['access_token']

def get_playlist_tracks(access_token, playlist_id):
    """Get all tracks from a playlist."""
    tracks = []
    url = f"{PLAYLIST_ENDPOINT}{playlist_id}/tracks"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error getting tracks: {response.text}")
            return tracks
        
        data = response.json()
        track_uris = [item['track']['uri'] for item in data['items'] if item['track'] is not None]
        tracks.extend(track_uris)
        
        url = data.get('next')
    
    return tracks

def clear_playlist(access_token, playlist_id):
    """Remove all tracks from a playlist."""
    url = f"{PLAYLIST_ENDPOINT}{playlist_id}/tracks"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'uris': []
    }
    
    # First get current tracks to know what to remove
    tracks = get_playlist_tracks(access_token, playlist_id)
    if not tracks:
        return True
    
    # Spotify API only allows removing 100 tracks at a time
    for i in range(0, len(tracks), 100):
        batch = tracks[i:i+100]
        payload = {'tracks': [{'uri': uri} for uri in batch]}
        
        response = requests.delete(url, headers=headers, data=json.dumps(payload))
        if response.status_code not in [200, 201]:
            print(f"Error clearing playlist: {response.text}")
            return False
    
    return True

def add_tracks_to_playlist(access_token, playlist_id, track_uris):
    """Add tracks to a playlist."""
    url = f"{PLAYLIST_ENDPOINT}{playlist_id}/tracks"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Spotify API only allows adding 100 tracks at a time
    for i in range(0, len(track_uris), 100):
        batch = track_uris[i:i+100]
        payload = {'uris': batch}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code not in [200, 201]:
            print(f"Error adding tracks: {response.text}")
            return False
    
    return True

def get_user_id(access_token):
    """Get the current user's Spotify ID."""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(USER_ENDPOINT, headers=headers)
    if response.status_code != 200:
        print(f"Error getting user data: {response.text}")
        return None
    
    return response.json()['id']

def combine_playlists():
    """Main function to combine playlists."""
    print(f"Starting playlist combination at {datetime.now().isoformat()}")
    
    # Get access token
    access_token = get_access_token()
    if not access_token:
        print("Failed to get access token")
        return False
    
    # Get tracks from source playlists
    discover_tracks = get_playlist_tracks(access_token, DISCOVER_WEEKLY_ID)
    release_tracks = get_playlist_tracks(access_token, RELEASE_RADAR_ID)
    
    print(f"Found {len(discover_tracks)} tracks in Discover Weekly")
    print(f"Found {len(release_tracks)} tracks in Release Radar")
    
    # Combine and deduplicate tracks
    all_tracks = list(set(discover_tracks + release_tracks))
    print(f"Combined playlist will have {len(all_tracks)} unique tracks")
    
    # Clear destination playlist
    print("Clearing destination playlist...")
    if not clear_playlist(access_token, COMBINED_PLAYLIST_ID):
        print("Failed to clear destination playlist")
        return False
    
    # Add tracks to destination playlist
    print("Adding tracks to destination playlist...")
    if not add_tracks_to_playlist(access_token, COMBINED_PLAYLIST_ID, all_tracks):
        print("Failed to add tracks to destination playlist")
        return False
    
    print(f"Successfully combined playlists at {datetime.now().isoformat()}")
    return True

if __name__ == "__main__":
    combine_playlists()
