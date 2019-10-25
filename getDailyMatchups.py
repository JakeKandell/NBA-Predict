# getDailyMatchups.py - Finds the daily NBA games

from nba_api.stats.endpoints import leaguegamelog, scoreboard
from teamIds import teams
from customHeaders import customHeaders

# Function to get you the games on a specified date (Home vs. Away)
# Used for dates in the past
# Return value is a list where index 0 is a dict holding the games and index 1 is the result of the games
# Enter a date in the format mm/dd/yyyy and season in the format yyyy-yy
def dailyMatchupsPast(date, season):

    # Obtains a list of teams who played on specified date
    dailyMatchups = leaguegamelog.LeagueGameLog(season=season, league_id='00', season_type_all_star='Regular Season', date_from_nullable=date,date_to_nullable=date, headers=customHeaders,timeout=60)
    dailyMatchupsDict = dailyMatchups.get_normalized_dict()
    listOfTeams = dailyMatchupsDict['LeagueGameLog']

    winLossList = []
    homeAwayDict = {}
    for i in range(0,len(listOfTeams),2):  # Loops through every other team
        if '@' in listOfTeams[i]['MATCHUP']:  # @ in matchup indicates that the current team is away
            awayTeam = listOfTeams[i]['TEAM_NAME']
            homeTeam = listOfTeams[i+1]['TEAM_NAME']

            winLossList.append(listOfTeams[i+1]['WL'])  # Appends if the home team won or lost to list

        else:
            awayTeam = listOfTeams[i+1]['TEAM_NAME']
            homeTeam = listOfTeams[i]['TEAM_NAME']

            winLossList.append(listOfTeams[i]['WL'])  # Appends if the home team won or lost to the list

        homeAwayDict.update({homeTeam:awayTeam})  # Adds current game to list of all games for that day

    matchupsResultCombined = [homeAwayDict, winLossList]  # Combines games and win/loss results into one list
    return(matchupsResultCombined)


# Function to get you the games on a specified date (Home vs. Away)
# Used for dates in the present or future
# Return value is a list where index 0 is a dict holding the games  {Home:Away}
# Enter a date in the format mm/dd/yyyy
def dailyMatchupsPresent(date):

    # Obtains all games that are set to occur on specified date
    dailyMatchups = scoreboard.Scoreboard(league_id='00', game_date=date, headers=customHeaders, timeout=60)
    dailyMatchupsDict = dailyMatchups.get_normalized_dict()
    listOfGames = dailyMatchupsDict['GameHeader']

    homeAwayDict = {}

    for game in listOfGames:  # Loops through each game on date

        homeTeamID = game['HOME_TEAM_ID']

        for team, teamID in teams.items():  # Finds name of the home team that corresponds with teamID
            if teamID == homeTeamID:
                homeTeamName = team

        awayTeamID = game['VISITOR_TEAM_ID']

        for team, teamID in teams.items():  # Finds name of the away team that corresponds with teamID
            if teamID == awayTeamID:
                awayTeamName = team

        homeAwayDict.update({homeTeamName:awayTeamName})

    return homeAwayDict
