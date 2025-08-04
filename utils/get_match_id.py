def get_match_id(home_team: str, away_team: str, start: str) -> str:
    """
    Generate a unique match ID based on the home and away team names and start time.

    Args:
        home_team (str): The name of the home team.
        away_team (str): The name of the away team.
        start (str): The start time of the match in ISO format.
        
    Returns:
        str: A unique match ID in the format "home_vs_away".

    Example:
        >>> get_match_id("Liverpool", "Bournemouth", "2025-08-15T19:00:00.000Z")
        LIV-BOU2025-08-15
    """
    return f"{home_team[:3].upper()}-{away_team[:3].upper()}{start[:10]}"