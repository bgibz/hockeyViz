import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from dateutil import tz
from util import jsonCleaner
from util import condensedGameTeamData


def clean_data(datafile):
    df = datafile + ".json"
    of = datafile + "_clean.json"
    inputfile = Path.cwd() / 'data' / df
    output = Path.cwd() / 'data' / of
    data_extract = jsonCleaner.JsonCleaner()
    data_extract.extract_game_data(inputfile, output)


def load_season(season):
    file_name = season + '_clean.json'
    file = Path.cwd() / 'data' / file_name
    with open(file) as f:
        data = f.read()
        json_data = json.loads(data)
        season_data = pd.DataFrame(json_data)
    return season_data


def add_game(_list, game, size):
    if len(_list) < size:
        _list.append(game)
    else:
        _list.pop(0)
        _list.append(game)


def check_dates(_list, num_games, date_range):
    if len(_list) == num_games:
        first = _list[0]
        last = _list[num_games-1]
        if (last.Date - first.Date).days < date_range:
            return True
    return False


def plot_wins_data(data, all_games, season, gd, folder, palette="RdYlGn"):
    my_dict = {
        "Team": data.team_name,
        "Games": data.gameCount,
        "Wins": data.wins,
        "Home": data.homeCount,
        "Home Wins": data.homeWins,
        "Away": data.awayCount,
        "Away Wins": data.awayWins
    }
    all_games[data.team_name] = my_dict
    df = pd.DataFrame(my_dict, index=[1])
    file = data.team_name + '.png'
    filepath = Path.cwd() / "Graphs" / season / folder / gd / file
    sns.barplot(data=df, palette=palette).set_title(data.team_name)
    plt.savefig(filepath)
    plt.clf()
    return all_games


def find_tired_games(season, num_games, num_days, from_zone=tz.gettz('UTC'), to_zone=tz.gettz('America/New_York')):
    results = {}
    buckets = {}
    for index, row in season.iterrows():
        raw_date = datetime.strptime(row.Date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=from_zone)
        row.Date = raw_date.astimezone(to_zone).date()
        buckets[row.Away] = buckets.get(row.Away, [])
        buckets[row.Home] = buckets.get(row.Home, [])
        add_game(buckets[row.Away], row, num_games)
        add_game(buckets[row.Home], row, num_games)
        if check_dates(buckets[row.Away], num_games, num_days):
            away_data = results.get(row.Away, condensedGameTeamData.CondensedGameTeamData(row.Away))
            away_data.update(row)
            results[row.Away] = away_data
        if check_dates(buckets[row.Home], num_games, num_days):
            home_data = results.get(row.Home, condensedGameTeamData.CondensedGameTeamData(row.Home))
            home_data.update(row)
            results[row.Home] = home_data
    return results


def find_tired_opponents(season, num_games, num_days, from_zone=tz.gettz('UTC'), to_zone=tz.gettz('America/New_York')):
    results = {}
    buckets = {}
    for index, row in season.iterrows():
        raw_date = datetime.strptime(row.Date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=from_zone)
        row.Date = raw_date.astimezone(to_zone).date()
        buckets[row.Away] = buckets.get(row.Away, [])
        buckets[row.Home] = buckets.get(row.Home, [])
        add_game(buckets[row.Away], row, num_games)
        add_game(buckets[row.Home], row, num_games)
        away_tired = check_dates(buckets[row.Away], num_games, num_days)
        home_tired = check_dates(buckets[row.Home], num_games, num_days)
        if away_tired and home_tired:
            pass
        elif away_tired and not home_tired:
            home_data = results.get(row.Home, condensedGameTeamData.CondensedGameTeamData(row.Home))
            home_data.update(row)
            results[row.Home] = home_data
        elif home_tired and not away_tired:
            away_data = results.get(row.Away, condensedGameTeamData.CondensedGameTeamData(row.Away))
            away_data.update(row)
            results[row.Away] = away_data
    return results


def process_tired_games(season, num_games, num_days):
    games_in_days = str(num_games) + 'in' + str(num_days)
    szn = load_season(season)
    extract = find_tired_games(szn, num_games, num_days)
    szn_tired_games = {}
    for data in extract:
        szn_tired_games = plot_wins_data(extract[data], szn_tired_games, season, games_in_days, folder="tired")
    szn_data = pd.DataFrame.from_dict(szn_tired_games, orient='index')
    szn_data.sort_values(by=["Games"], inplace=True)
    # Plot stuff
    sns.color_palette("magma", as_cmap=True)
    szn_plot = sns.barplot(y="Team", x="Games", data=szn_data)
    name = season + ".png"
    filepath = Path.cwd() / "Graphs" / season / "tired" / games_in_days / name
    plt.tight_layout()
    plt.savefig(filepath)
    plt.clf()
    # Save a csv
    name = season + ".csv"
    filepath = Path.cwd() / "Graphs" / season / "tired" / games_in_days / name
    szn_data.to_csv(filepath)


def process_tired_opponents(season, num_games, num_days):
    games_in_days = str(num_games) + 'in' + str(num_days)
    szn = load_season(season)
    extract = find_tired_opponents(szn, num_games, num_days)
    szn_tired_games = {}
    for data in extract:
        szn_tired_games = plot_wins_data(extract[data], szn_tired_games, season, games_in_days,
                                         folder="tired_opponents", palette="gist_stern")
    szn_data = pd.DataFrame.from_dict(szn_tired_games, orient='index')
    szn_data.sort_values(by=["Games"], inplace=True)
    # Plot stuff
    szn_plot = sns.barplot(y="Team", x="Games", data=szn_data, palette="mako")
    name = season + ".png"
    filepath = Path.cwd() / "Graphs" / season / "tired_opponents" / games_in_days / name
    plt.tight_layout()
    plt.savefig(filepath)
    plt.clf()
    # Save a csv
    name = season + ".csv"
    filepath = Path.cwd() / "Graphs" / season / "tired_opponents" / games_in_days / name
    szn_data.to_csv(filepath)

# 3 in 4 from 2018-19 season
season = "201819"
num_games = 2
num_days = 2

process_tired_games(season, num_games, num_days)


print("Done.")
