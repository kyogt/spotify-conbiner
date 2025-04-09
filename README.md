# Spotify Playlist Combiner

This repository automatically combines tracks from Spotify's "Discover Weekly" and "Release Radar" playlists into a single "Combined Playlist" every Monday using GitHub Actions.

## How It Works

1. Every Monday, the GitHub Actions workflow runs automatically
2. The script retrieves tracks from your "Discover Weekly" and "Release Radar" playlists
3. It clears the "Combined Playlist" and adds all unique tracks from both source playlists
4. The combined playlist is available on your Spotify account

## Repository Setup

This repository uses GitHub Actions to run the script on a schedule without requiring a local environment.

### Required Environment Variables

The following secrets need to be set in the repository settings:

- `SPOTIFY_CLIENT_ID`: Your Spotify application client ID
- `SPOTIFY_CLIENT_SECRET`: Your Spotify application client secret
- `SPOTIFY_REFRESH_TOKEN`: A refresh token with permissions to modify your playlists

## How to Obtain a Refresh Token

To obtain a refresh token for your Spotify account, follow these steps:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Create a new application (if you haven't already)
3. Set the redirect URI to `http://localhost:8000` (or any available local port)
4. Copy your Client ID and Client Secret
5. Use the following URL in your browser (replace CLIENT_ID with yours):
```
https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:8000&scope=playlist-read-private%20playlist-modify-public%20playlist-modify-private
```
6. After authorizing, you'll be redirected to localhost with a code parameter in the URL
7. Use this code to request a refresh token with the following command (replace with your credentials):
```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=authorization_code&code=YOUR_CODE&redirect_uri=http://localhost:8000&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET" https://accounts.spotify.com/api/token
```
8. The response will include a refresh token that you should save
