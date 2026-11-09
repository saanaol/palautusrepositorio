class PlayerStats:
    def __init__(self, reader):
        self._players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        players = []

        for player in self._players:
            if player.nationality == nationality:
                players.append(player)

        return sorted(
            players,
            key=lambda player: player.goals + player.assists,
            reverse=True
        )

    def get_nationalities(self):
        nationalities = set()

        for player in self._players:
            nationalities.add(player.nationality)

        return sorted(nationalities)
