import sys, os
sys.path.append('D:/Python/nba')

import numpy as np
import pandas as pd
from nba_data_pull import get_nba_team_stats

reg_season_df = get_nba_team_stats(2011)
print(reg_season_df.head())