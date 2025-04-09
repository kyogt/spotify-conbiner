# Spotify Playlist Combiner

This repository automatically combines tracks from Spotify's "Discover Weekly" and "Release Radar" playlists into a single "Combined Playlist" every Monday using GitHub Actions.

## How It Works

1. Every Monday, the GitHub Actions workflow runs automatically
2. The script retrieves tracks from your "Discover Weekly" and "Release Radar" playlists
3. It clears the "Combined Playlist" and adds all unique tracks from both source playlists
4. The combined playlist is available on your Spotify account

## Setup Instructions

### 1. Configure Your Spotify Developer App

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Find your app (with Client ID: 4d54bc8c7d244ea090e787329ad1ffe0)
4. Click on "Edit Settings"
5. Add `http://localhost:8000` as a Redirect URI
6. Save your changes

### 2. Get Your Spotify Refresh Token

There are two ways to get your refresh token:

#### Option A: Using the interactive script
Run the `simple_auth.py` script:
```
python simple_auth.py
```
Follow the prompts to:
1. Generate an authorization URL
2. Open the URL in your browser and authorize the app
3. Copy the authorization code from the redirected URL
4. Exchange it for a refresh token

#### Option B: Using the automated script
If the redirect URI is properly configured, you can use:
```
python get_refresh_token.py
```
This will automatically open your browser and retrieve the token.

### 3. Configure GitHub Repository Secrets

1. Go to your repository: Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `SPOTIFY_CLIENT_ID`: 4d54bc8c7d244ea090e787329ad1ffe0
   - `SPOTIFY_CLIENT_SECRET`: 5a6aa2dc55534855864341e9e598ddbd
   - `SPOTIFY_REFRESH_TOKEN`: (the refresh token you obtained in step 2)

### 4. Setup GitHub Actions Workflow

You need to create the workflow file in the correct location through the GitHub web interface:

1. Go to your repository on GitHub
2. Click "Add file" > "Create new file"
3. Enter `.github/workflows/weekly_combine.yml` as the file name
4. Copy and paste the following content:

```yaml
name: Weekly Spotify Playlist Combiner

on:
  schedule:
    - cron: '0 8 * * 1'  # Run at 8:00 AM every Monday
  workflow_dispatch:     # Allow manual trigger

jobs:
  combine-playlists:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run playlist combiner
      env:
        SPOTIFY_CLIENT_ID: ${{ secrets.SPOTIFY_CLIENT_ID }}
        SPOTIFY_CLIENT_SECRET: ${{ secrets.SPOTIFY_CLIENT_SECRET }}
        SPOTIFY_REFRESH_TOKEN: ${{ secrets.SPOTIFY_REFRESH_TOKEN }}
      run: python spotify_combiner.py
```

5. Commit the new file
6. You can then delete the `weekly_combine.yml` file from the root directory if desired

### 5. Test the Workflow

1. Go to the Actions tab in your repository
2. Find the "Weekly Spotify Playlist Combiner" workflow
3. Click "Run workflow" to test it manually

Once set up, the workflow will automatically run every Monday at 8:00 AM UTC, combining your playlists.

## Troubleshooting

If you encounter any issues:

1. Check the Actions tab to see the workflow logs
2. Make sure your secrets are correctly set in the repository settings
3. Ensure your Spotify refresh token is valid
4. Verify that the playlist IDs in the script match your playlists
