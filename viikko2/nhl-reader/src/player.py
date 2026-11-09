class Player:
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.team = player_dict['team']
        self.goals = player_dict['goals']
        self.assists = player_dict['assists']
        self.nationality = player_dict['nationality']

    def __str__(self):
        return (
            f'{self.name:25} {self.team:15} '
            f'{self.goals} + {self.assists} = '
            f'{self.goals + self.assists}'
        )
