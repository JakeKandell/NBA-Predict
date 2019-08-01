# nbaPredict.py - Predicts results of NBA games on a specified date
# Call makeInterpretPrediction with current date, season, and start date of season to run predictions

import os
import pickle
import pandas as pd

from getDailyMatchups import dailyMatchups
from createModel import createMeanStandardDeviationDicts
from availableStats import availableStats
from createModel import zScoreDifferential
from getStats import getStatsForTeam

# CHANGE CURRENT WORKING DIRECTORY HERE TO WHEREVER THE MODEL IS SAVED
os.chdir('/Users/JakeKandell/Desktop/NBA-Predict/SavedModels/')


# Returns list of games with Z-Score differentials between teams to be put into a Pandas dataframe
# startDate & endDate should be 'mm/dd/yyyy' form
def dailyGamesDataFrame(dailyGames, meanDict, standardDeviationDict, startDate, endDate):

    fullDataFrame = []

    for homeTeam,awayTeam in dailyGames.items():

        homeTeamStats = getStatsForTeam(homeTeam, startDate, endDate)
        awayTeamStats = getStatsForTeam(awayTeam, startDate, endDate)

        currentGame = [homeTeam,awayTeam]

        for stat,statType in availableStats.items():  # Finds Z Score Dif for stats listed above and adds them to list
            zScoreDif = zScoreDifferential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
            currentGame.append(zScoreDif)

        fullDataFrame.append(currentGame)  # Adds this list to list of all games on specified date

    return(fullDataFrame)


# Returns a list
# Index 0 is the dailyGames in dict form {Home:Away}
# Index 1 is a list with the prediction probabilities for each game [[lossProb, winProb]]
# currentDate should be in form 'mm/dd/yyyy' and season in form 'yyyy-yy'
def predictDailyGames(currentDate, season, startOfSeason):

    dailyGames = dailyMatchups(currentDate, season, False)  # False because games should be on current date not in past
    meanDict, standardDeviationDict = createMeanStandardDeviationDicts(startOfSeason, currentDate)
    dailyGamesList = dailyGamesDataFrame(dailyGames, meanDict, standardDeviationDict, startOfSeason, currentDate)

    # Pandas dataframe holding daily games and Z-Score differentials between teams
    gamesWithZScoreDifs = pd.DataFrame(
        dailyGamesList,
        columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
    )

    justZScoreDifs = gamesWithZScoreDifs.loc[:,'W_PCT':'TS_PCT']  # Slices only the features used in the model

    with open('finalized_model.pkl', 'rb') as file:  # Change filename here if model is named differently
        pickleModel = pickle.load(file)

    predictions = pickleModel.predict_proba(justZScoreDifs)  # Predicts the probability that the home team loses/wins

    gamesWithPredictions = [dailyGames, predictions]
    return gamesWithPredictions


# Returns the percent chance that the home team will defeat the away team for each game
# gamesWithPredictions should be in form [dailyGames, predictionsList]
def interpretPredictions(gamesWithPredictions):

    dailyGames = gamesWithPredictions[0]  # Dict holding daily matchups
    probabilityPredictions = gamesWithPredictions[1]  # List of lists holding probs of loss/win for home team

    for gameNum in range(len(probabilityPredictions)):  # Loops through each game
        winProb = probabilityPredictions[gameNum][1]
        winProbRounded = round(winProb,4)
        winProbPercent = "{:.2%}".format(winProbRounded)  # Formulates percent chance that home team wins

        homeTeam = list(dailyGames.keys())[gameNum]
        awayTeam = list(dailyGames.values())[gameNum]

        print('There is a ' + winProbPercent + ' chance that the ' + homeTeam + ' will defeat the ' + awayTeam + '.')


# Fetches games on set date and returns predictions for each game
# currentDate/startOfSeason should be in form 'mm/dd/yyyy' and season in form 'yyyy-yy'
# Start of 2018-19 season was 10/16/2018
def makeInterpretPredictions(currentDate, season, startOfSeason):

    predictions = predictDailyGames(currentDate, season, startOfSeason)
    interpretPredictions(predictions)


makeInterpretPredictions('01/28/2019', '2018-19', '10/16/2018')