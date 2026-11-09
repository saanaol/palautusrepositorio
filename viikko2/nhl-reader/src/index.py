from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats


def print_players(players, season, nationality):
    table = Table(
        title=f'Season {season} players from {nationality}',
        title_style='italic',
        header_style='bold white',
        box=box.SQUARE
    )

    table.add_column('Player', style='cyan')
    table.add_column('teams', style='magenta')
    table.add_column('goals', justify='right', style='green')
    table.add_column('assists', justify='right', style='green')
    table.add_column('points', justify='right', style='green')

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists)
        )

    console = Console()
    console.print(table)

def ask_season():
    seasons = [
        '2018-19', '2019-20', '2020-21', '2021-22',
        '2022-23', '2023-24', '2024-25', '2025-26'
    ]

    return Prompt.ask(
        'Season',
        choices=seasons,
        default='2024-25'
    )

def main():
    season = ask_season()

    url = f'https://studies.cs.helsinki.fi/nhlstats/{season}/players'
    stats = PlayerStats(PlayerReader(url))
    nationalities = stats.get_nationalities()

    while True:
        nationality = Prompt.ask(
            'Nationality (q quits)',
            choices=nationalities + ['q'],
            case_sensitive=False
        ).upper()

        if nationality == 'Q':
            break

        players = stats.top_scorers_by_nationality(nationality)
        print_players(players, season, nationality)


if __name__ == "__main__":
    main()
