import unittest

from player import Player
from player_stats import PlayerStats


class PlayerReaderStub:
    def __init__(self, players):
        self._players = players

    def get_players(self):
        return self._players


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        players = [
            Player({
                'name': 'Connor',
                'team': 'COL, CAR, DAL',
                'goals': 40,
                'assists': 60,
                'nationality': 'CAN'
            }),
            Player({
                'name': 'Alex',
                'team': 'COL',
                'goals': 50,
                'assists': 40,
                'nationality': 'CAN'
            }),
            Player({
                'name': 'Bobby',
                'team': 'DAL, CAR',
                'goals': 60,
                'assists': 10,
                'nationality': 'CAN'
            }),
            Player({
                'name': 'Finn',
                'team': 'CAR',
                'goals': 35,
                'assists': 40,
                'nationality': 'FIN'
            }),
            Player({
                'name': 'Evan',
                'team': 'DAL, COL, CAR',
                'goals': 25,
                'assists': 30,
                'nationality': 'FIN'
            })
        ]
        self.stats = PlayerStats(PlayerReaderStub(players))

    def test_top_scorers_by_nationality_returns_players_in_points_order(self):
        players = self.stats.top_scorers_by_nationality('CAN')

        self.assertEqual([player.name for player in players], ['Connor', 'Alex', 'Bobby'])
        self.assertEqual(len(players), 3)

    def test_top_scorers_by_nationality_returns_empty_list_when_no_players_match(self):
        players = self.stats.top_scorers_by_nationality('SWE')

        self.assertEqual(players, [])

    def test_get_nationalities_returns_sorted_unique_nationalities(self):
        nationalities = self.stats.get_nationalities()

        self.assertEqual(nationalities, ['CAN', 'FIN'])

    def test_top_scorers_by_team_matches_all_codes_and_sorts_by_points(self):
        players = self.stats.top_scorers_by_team('DAL')

        self.assertEqual(
            [player.name for player in players],
            ['Connor', 'Bobby', 'Evan']
        )
        self.assertEqual(len(players), 3)

    def test_top_scorers_by_team_returns_empty_list_when_no_players_match(self):
        players = self.stats.top_scorers_by_team('SWE')

        self.assertEqual(players, [])

    def test_top_goal_scorers_returns_requested_count_in_goals_order(self):
        players = self.stats.top_goal_scorers(3)

        self.assertEqual([player.name for player in players], ['Bobby', 'Alex', 'Connor'])
        self.assertEqual(len(players), 3)

    def test_top_goal_scorers_returns_empty_list_when_count_is_zero(self):
        players = self.stats.top_goal_scorers(0)

        self.assertEqual(players, [])
