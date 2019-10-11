# standardizeStats.py - Uses Z Scores ((Obs  - Mean) / St Dev.) to standardize any of the different statistics scraped

from nba_api.stats.endpoints import leaguedashteamstats
import statistics
from getStats import getStatsForTeam
import time
from customHeaders import customHeaders

# Finds league mean for the entered basic or advanced statistic (statType = 'Base' or 'Advanced')
def basicOrAdvancedStatMean(startDate, endDate, stat,statType = 'Base', season='2018-19'):

    time.sleep(.2)
    # Gets list of dictionaries with stats for every team
    allTeamsInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
                                                           measure_type_detailed_defense=statType,
                                                           date_from_nullable=startDate,
                                                           date_to_nullable=endDate,
                                                           season=season,
                                                           headers=customHeaders,
                                                           timeout=120)
    allTeamsDict = allTeamsInfo.get_normalized_dict()
    allTeamsList = allTeamsDict['LeagueDashTeamStats']

    specificStatAllTeams = []
    for i in range(len(allTeamsList)):  # Loops through and appends specific stat to new list until every team's stat has been added
        specificStatAllTeams.append(allTeamsList[i][stat])

    mean = statistics.mean(specificStatAllTeams)  # Finds mean of stat
    return mean


# Finds league standard deviation for the entered basic or advanced statistic (statType = 'Base' or 'Advanced')
def basicOrAdvancedStatStandardDeviation(startDate, endDate, stat,statType = 'Base', season='2018-19'):

    time.sleep(.2)
    # Gets list of dictionaries with stats for every team
    allTeamsInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
                                                           measure_type_detailed_defense=statType,
                                                           date_from_nullable=startDate,
                                                           date_to_nullable=endDate,
                                                           season=season,
                                                           headers=customHeaders,
                                                           timeout=120
                                                           )
    allTeamsDict = allTeamsInfo.get_normalized_dict()
    allTeamsList = allTeamsDict['LeagueDashTeamStats']

    specificStatAllTeams = []
    for i in range(len(allTeamsList)):  # Loops and appends specific stat to new list until every team's stat has been added
        specificStatAllTeams.append(allTeamsList[i][stat])

    standardDeviation = statistics.stdev(specificStatAllTeams)  # Finds standard deviation of stat
    return standardDeviation


# Returns a standardized version of each data point via the z-score method
def basicOrAdvancedStatZScore(observedStat, mean, standardDeviation):

    zScore = (observedStat-mean)/standardDeviation  # Calculation for z-score

    return(zScore)

