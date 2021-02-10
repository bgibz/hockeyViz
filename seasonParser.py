import json


class SeasonParser:
    def load_season(self, input):
        with open(input_file_path) as f:
            data = f.read()
            json_data = json.loads(data)

