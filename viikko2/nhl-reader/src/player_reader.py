import requests
from player import Player


class PlayerReader:
    def __init__(self, url):
        self._url = url

    def get_players(self):
        response = requests.get(self._url, timeout=30)
        response.raise_for_status()
        player_data = response.json()

        players = []

        for player_dict in player_data:
            player = Player(player_dict)
            players.append(player)

        return players
