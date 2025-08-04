import requests
import datetime

sports_db_base_url = "https://www.thesportsdb.com/api/v1/json/123/eventsseason.php"

def fetch_matches(
        league_id: int = 4332,  # Serie A league ID
        seasonFrom: int = datetime.datetime.now().year,
        seasonTo: int = datetime.datetime.now().year + 1
):
    """
    Fetch a specified league events from the database.

    Returns:
        list: A list of a specified league events.
    """
    response = requests.get(f"{sports_db_base_url}?id={league_id}&s={seasonFrom}-{seasonTo}")
    if response.status_code == 200:
        data = response.json()
        if "events" in data:
            # From each event we only need strHomeTeam, strAwayTeam and strTimestamp
            return [
                {
                    "home_team": event["strHomeTeam"],
                    "away_team": event["strAwayTeam"],
                    "timestamp": event["strTimestamp"]
                }
                for event in data["events"]
            ]
        return data.get("events", [])
    return []