from pybaseball import batting_stats_range
from pybaseball import pitching_stats_range
from pybaseball import statcast_batter
p_data = statcast_batter('2022-10-30', '2023-04-25', 663538)
#p_data = pitching_stats_range("2021-10-01", "2023-04-25")
#b_data = batting_stats_range("2021-10-01", "2023-04-25")
#b_data.to_csv('backend/flask/current_batting.csv', index=False)
p_data.to_csv('backend/flask/current_stat.csv', index=False)