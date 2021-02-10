import json


class JsonCleaner:
    def __init__(self):
        self.filePath = None

    def extract_game_data(self, input_file_path, output_file_path):
        output = []
        with open(input_file_path) as f:
            data = f.read()
            json_data = json.loads(data)
            # iterate over dates array, extract all games
            for date in json_data.get("dates"):
                # iterate over games
                for game in date.get("games"):
                    if game["gameType"] == "R":
                        data = self.game_data(game)
                        output.append(data)
        with open(output_file_path, 'w') as file:
            file.write(json.dumps(output))

    @staticmethod
    def game_data(game):
        game_id = game["gamePk"]
        home = game["teams"]["home"]["team"]["name"]
        away = game["teams"]["away"]["team"]["name"]
        home_score = game["teams"]["home"]["score"]
        away_score = game["teams"]["away"]["score"]
        winner = home if home_score > away_score else away
        if home_score == away_score:
            print("Found a tie")
        data = {
            "Date": game["gameDate"],
            "Away": away,
            "AwayScore": away_score,
            "Home": home,
            "HomeScore": home_score,
            "Winner": winner,
            "ID": game_id
        }
        return data

