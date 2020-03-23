import numpy as np
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats

def get_nba_team_stats (start_year,type='regular'):
    # Getting Mavs team ID for example
    nba_teams = teams.get_teams()
    mavs_id = [team for team in nba_teams
            if team['full_name'] == 'Dallas Mavericks'][0]

    # Get Mavs reg season yby DF to create empty DF with appropriate columns
    reg_season_yby_mavs = teamyearbyyearstats.TeamYearByYearStats(team_id=mavs_id['id']).get_data_frames()[0]
    reg_season_yby = pd.DataFrame(columns=reg_season_yby_mavs.columns)

    # Get Reg Season YBY stats for all teams, beginning in 2011-12
    for team in nba_teams :
        team_yby_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team['id']).get_data_frames()[0]
        team_yby_stats['START_YEAR'] = team_yby_stats['YEAR']
        start_year_index = team_yby_stats[team_yby_stats['YEAR'].str.slice(stop=4) == str(start_year)].index.values[0]
        team_yby_stats = team_yby_stats[(team_yby_stats.index > start_year_index)]
        reg_season_yby = reg_season_yby.append(team_yby_stats,sort=True)

    print('Number of unique team IDs: ', reg_season_yby['TEAM_ID'].nunique())
    reg_season_yby = reg_season_yby.set_index(['TEAM_ID', 'YEAR'])
    return reg_season_yby
