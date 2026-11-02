import unittest
from statistics_service import StatisticsService, SortBy
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(PlayerReaderStub())

    def test_search_palauttaa_loytyvan_pelaajan(self):
        player = self.stats.search("Kurri")
        self.assertEqual(player.name, "Kurri")
        self.assertEqual(player.team, "EDM")

    def test_search_palauttaa_none_jos_pelaajaa_ei_loydy(self):
        player = self.stats.search("Tuntematon")
        self.assertIsNone(player)

    def test_team_palauttaa_joukkueen_pelaajat(self):
        players = self.stats.team("EDM")

        self.assertEqual([player.name for player in players], ["Semenko", "Kurri", "Gretzky"])

    def test_team_palauttaa_tyhjan_listan_jos_joukkuetta_ei_loydy(self):
        players = self.stats.team("XYZ")
        self.assertEqual(players, [])

    def test_top_palauttaa_kolme_parasta_pistejarjestyksessa(self):
        players = self.stats.top(3)
        self.assertEqual([player.name for player in players], ["Gretzky", "Lemieux", "Yzerman"])

    def test_top_nolla_palauttaa_tyhjan_listan(self):
        players = self.stats.top(0)
        self.assertEqual(players, [])

    def test_top_pisteiden_mukaan(self):
        players = self.stats.top(3, SortBy.POINTS)
        self.assertEqual([player.name for player in players], ["Gretzky", "Lemieux", "Yzerman"])

    def test_top_maalien_mukaan(self):
        players = self.stats.top(3, SortBy.GOALS)
        self.assertEqual([player.name for player in players], ["Lemieux", "Yzerman", "Kurri"])

    def test_top_syottojen_mukaan(self):
        players = self.stats.top(3, SortBy.ASSISTS)
        self.assertEqual([player.name for player in players], ["Gretzky", "Yzerman", "Lemieux"])
