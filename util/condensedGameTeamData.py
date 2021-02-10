class CondensedGameTeamData:
    def __init__(self, team_name):
        self.team_name = team_name
        self.gameCount = 0
        self.homeCount = 0
        self.homeWins = 0
        self.awayCount = 0
        self.awayWins = 0
        self.wins = 0
        self.gameIds = []

    def update(self, game_data):
        if game_data["ID"] not in self.gameIds:
            self.gameIds.append(game_data["ID"])
            self.gameCount += 1
            if self.team_name == game_data["Home"]:
                self.homeCount += 1
                if self.team_name == game_data["Winner"]:
                    self.wins += 1
                    self.homeWins += 1
            else:
                self.awayCount += 1
                if self.team_name == game_data["Winner"]:
                    self.wins += 1
                    self.awayWins += 1
