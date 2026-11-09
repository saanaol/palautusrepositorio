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

    def top_goal_scorers(self, how_many):
        """Palauttaa how_many parasta maalintekijää maalimäärän mukaan."""
        return sorted(
            self._players,
            key=lambda player: player.goals,
            reverse=True
        )[:how_many]

    def top_scorers_by_team(self, team):
        teams = {team_code.strip() for team_code in team.split(',')}
        players = []

        for player in self._players:
            player_teams = {
                team_code.strip() for team_code in player.team.split(',')
            }
            if teams.issubset(player_teams):
                players.append(player)

        return sorted(
            players,
            key=lambda player: player.goals + player.assists,
            reverse=True
        )
