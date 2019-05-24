import numpy as np
import pandas as pd

from nba_api.stats.static import teams
# get_teams returns a list of 30 dictionaries, each an NBA team.
nba_teams = teams.get_teams()
print('Number of teams fetched: {}'.format(len(nba_teams)))
mavs_id = [team for team in nba_teams
         if team['full_name'] == 'Dallas Mavericks'][0]

# Get Mavs reg season yby DF to create empty DF with appropriate columns
from nba_api.stats.endpoints import teamyearbyyearstats
reg_season_yby_mavs = teamyearbyyearstats.TeamYearByYearStats(team_id=mavs_id['id']).get_data_frames()[0]
reg_season_yby = pd.DataFrame(columns=reg_season_yby_mavs.columns)

print(reg_season_yby)

# Get Reg Season YBY stats for all teams, beginning in 2011-12
for team in nba_teams :
    team_yby_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team['id']).get_data_frames()[0]
    lockout_year_index = team_yby_stats[team_yby_stats['YEAR'] == '2011-12'].index.values[0]
    team_yby_stats = team_yby_stats[(team_yby_stats.index > lockout_year_index) & (team_yby_stats['GP'] > 69)]
    reg_season_yby = reg_season_yby.append(team_yby_stats)

print(reg_season_yby.head())
print(reg_season_yby.describe())
print(reg_season_yby.shape)
reg_season_yby['TEAM_CITY'].nunique()
reg_season_yby = reg_season_yby.set_index(['TEAM_ID', 'YEAR'])
reg_season_yby.to_csv('D:\\Python\\zstorage\\nba\\reg_season_yby.csv')

