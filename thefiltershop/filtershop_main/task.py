import requests
from filtershop_main.models import Entry_on_Steam

def populate_steam_entries():
    # Fetch list of all games from the Steam API
        steam_api_url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response = requests.get(steam_api_url)
        data = response.json()

        # Populate the model
        for app_data in data['applist']['apps']:
            app_id = app_data['appid']
            app_name = app_data['name']

            # Update or create the model entry
            Entry_on_Steam.objects.update_or_create(
                app_id=app_id,
                defaults={'name': app_name}
            )