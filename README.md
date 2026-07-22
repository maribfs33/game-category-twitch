# Twitch Category Monitor

A lightweight, 100% free Twitch stream category monitor built with Python, GitHub Actions, and Discord Webhooks. 

It checks a streamer's live status every 5 minutes and automatically posts an alert to your Discord server whenever they change their streaming category or game.

---

## Features

* **Zero Hosting Costs:** Runs entirely on GitHub Actions without needing a 24/7 dedicated server or local machine.
* **Automated Checking:** Runs every 5 minutes via GitHub Workflows (cron schedule).
* **Rich Discord Alerts:** Sends styled embeds with the stream title, new category name, and stream link.
* **State Tracking:** Uses a simple JSON file committed back to the repository to track stream changes across workflow runs.

---

## Project Structure

* `.github/workflows/monitor.yml` - GitHub Actions schedule & script trigger
* `monitor.py` - Python script for Twitch API & Webhook execution
* `state.json` - Stores current live state and last category
* `README.md` - Project documentation

---

## Setup Instructions

### 1. Discord Webhook
1. Go to **Server Settings** -> **Integrations** -> **Webhooks** in your Discord server.
2. Create a new webhook and copy its URL.

### 2. Twitch Credentials
1. Register an application on the [Twitch Developer Console](https://dev.twitch.tv/console).
2. Set OAuth Redirect URL to `http://localhost`.
3. Obtain your **Client ID** and generate a new **Client Secret**.

### 3. Repository Secrets
In your GitHub repository, navigate to **Settings** -> **Secrets and variables** -> **Actions** and add four repository secrets:

* `TWITCH_CLIENT_ID`: Your Twitch Application Client ID
* `TWITCH_CLIENT_SECRET`: Your Twitch Application Client Secret
* `DISCORD_WEBHOOK_URL`: Your Discord Webhook URL
* `STREAMER_NAME`: The exact Twitch username to track

### 4. Permissions
Ensure GitHub Actions has permission to update `state.json`:
1. Go to **Settings** -> **Actions** -> **General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Save your changes.

---

## How It Works

1. **Trigger:** GitHub Actions triggers `monitor.py` every 5 minutes.
2. **Fetch:** The script requests stream details from the Twitch Helix API using Client Credentials.
3. **Compare:** It reads `state.json` to compare the current category against the previous record.
4. **Notify:** If a category change is detected during a live stream, a notification is sent to Discord via webhook.
5. **Update:** `state.json` is updated and committed back to the repository.
