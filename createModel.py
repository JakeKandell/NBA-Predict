# createModel.py - Used to train, test, and create the model
# Call createModel() to generate a new model
# May need to edit which lines are commented out based on what range of game data you would like to use

from standardizeStats import basicOrAdvancedStatZScore, basicOrAdvancedStatStandardDeviation, basicOrAdvancedStatMean
from getDailyMatchups import dailyMatchups
from getStats import getStatsForTeam
from availableStats import availableStats


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle

import os

from datetime import timedelta, date


# Calculates the zScore differential between two teams for a specified stat
def zScoreDifferential(observedStatHome, observedStatAway, mean, standardDeviation):

    homeTeamZScore = basicOrAdvancedStatZScore(observedStatHome, mean, standardDeviation)
    awayTeamZScore = basicOrAdvancedStatZScore(observedStatAway, mean, standardDeviation)

    differenceInZScore = homeTeamZScore - awayTeamZScore
    return differenceInZScore


# Used to combine and format all the data to be put into a pandas dataframe
# dailyGames should be list where index 0 is a dictionary holding the games and index 1 is a list holding the results
def infoToDataFrame(dailyGames, meanDict, standardDeviationDict, startDate, endDate):

    fullDataFrame = []
    gameNumber = 0  # Counter to match the result of the game with the correct game
    dailyResults = dailyGames[1]  # List of results for the games

    for homeTeam,awayTeam in dailyGames[0].items():

        homeTeamStats = getStatsForTeam(homeTeam, startDate, endDate)
        awayTeamStats = getStatsForTeam(awayTeam, startDate, endDate)

        currentGame = [homeTeam,awayTeam]

        for stat,statType in availableStats.items():  # Finds Z Score Dif for stats listed above and adds them to list
            zScoreDif = zScoreDifferential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
            currentGame.append(zScoreDif)

        if dailyResults[gameNumber] == 'W':  # Sets result to 1 if a win
            result = 1
        else :  # Sets result to 0 if loss
            result = 0

        currentGame.append(result)
        gameNumber += 1

        print(currentGame)
        fullDataFrame.append(currentGame)  # Adds this list to list of all games on specified date

    return(fullDataFrame)

# Function that allows iterating through specified start date to end date
def daterange(startDate, endDate):

    for n in range(int ((endDate - startDate).days)):
        yield startDate + timedelta(n)


# Returns a list. Index 0 is a dict holding mean for each stat. Index 1 is a dict holding standard deviation for each stat.
def createMeanStandardDeviationDicts(startDate, endDate):

    meanDict = {}
    standardDeviationDict = {}

    # Loops through and inputs standard deviation and mean for each stat into dict
    for stat, statType in availableStats.items():
        statMean = basicOrAdvancedStatMean(startDate, endDate, stat, statType)
        meanDict.update({stat: statMean})

        statStandardDeviation = basicOrAdvancedStatStandardDeviation(startDate, endDate, stat, statType)
        standardDeviationDict.update({stat: statStandardDeviation})

    bothDicts = []
    bothDicts.append(meanDict)
    bothDicts.append(standardDeviationDict)

    return bothDicts

# Loops through every date between start and end and appends each game to a singular list to be returned
def getTrainingSet(startYear, startMonth, startDay, endYear, endMonth, endDay):

    startDate = date(startYear, startMonth, startDay)
    endDate = date(endYear, endMonth, endDay)

    startDateFormatted = startDate.strftime("%m/%d/%Y")  # Formats start date in mm/dd/yyyy
    allGames = []

    for singleDate in daterange(startDate, endDate):
        currentDate = singleDate.strftime("%m/%d/%Y")  # Formats current date in mm/dd/yyyy
        print(currentDate)

        meanAndStandardDeviationDicts = createMeanStandardDeviationDicts('10/16/2018', currentDate)
        meanDict = meanAndStandardDeviationDicts[0]  # Dict in format {stat:statMean}
        standardDeviationDict = meanAndStandardDeviationDicts[1]  # Dict in format {stat:statStDev}

        currentDayGames = dailyMatchups(currentDate, '2018-19')  # Finds games on current date in loop
        currentDayGamesAndStatsList = infoToDataFrame(currentDayGames, meanDict, standardDeviationDict, '10/16/2018', currentDate)  # Formats Z Score difs for games on current date in loop

        for game in currentDayGamesAndStatsList:  # Adds game with stats to list of all games
            allGames.append(game)

    print(allGames)
    return(allGames)


# Returns a dataframe from list of games with z score differentials
def createDataFrame(listOfGames):

    games = pd.DataFrame(
        listOfGames,
        columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'Result']
    )

    print(games)
    return(games)


# Creates the logistic regression model and tests accuracy
def performLogReg(dataframe):

    # Update if new stats are added
    featureColumns = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    X = dataframe[featureColumns] # Features
    Y = dataframe.Result  # Target Variable

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, shuffle=True)
    logreg = LogisticRegression()

    logreg.fit(X_train, Y_train)  # Fits model with data

    Y_pred = logreg.predict(X_test)

    confusionMatrix = metrics.confusion_matrix(Y_test, Y_pred)  # Diagonals tell you correct predictions
    print(confusionMatrix)

    print("Accuracy:", metrics.accuracy_score(Y_test, Y_pred))
    print("Precision:", metrics.precision_score(Y_test, Y_pred))
    print("Recall:", metrics.recall_score(Y_test, Y_pred))

    print(featureColumns)
    print(logreg.coef_)

    return logreg


# Saves the model in folder to be used in future
def saveModel(model):

    # Change to where you want to save the model
    os.chdir('/Users/JakeKandell/Desktop/NBA-Predict/SavedModels/')

    filename = 'abc.pkl'
    with open(filename, 'wb') as file:
        pickle.dump(model, file)


def createModel(startYear=None, startMonth=None, startDay=None, endYear=None, endMonth=None, endDay=None):

    # allGames = getTrainingSet(startYear, startMonth, startDay, endYear, endMonth, endDay)  # Unnecessary if using data from CSV file

    # allGamesDataframe = createDataFrame(allGames)  # Unnecessary if using data from CSV file

    allGamesDataframe = pd.read_csv('/Users/JakeKandell/Desktop/NBA-Predict/Data/games.csv')  # Should be commented out if needing to obtain data on different range of games

    logRegModel = performLogReg(allGamesDataframe)

    saveModel(logRegModel)

