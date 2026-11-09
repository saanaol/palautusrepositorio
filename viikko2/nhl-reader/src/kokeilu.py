from player_reader import PlayerReader
from player_stats import PlayerStats


def main():
    url = 'https://studies.cs.helsinki.fi/nhlstats/2024-25/players'
    stats = PlayerStats(PlayerReader(url))

    for player in stats.top_scorers_by_team('DAL'):
        print(player)


if __name__ == '__main__':
    main()
