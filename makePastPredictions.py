# makePastPredictions.py - Used to predicts specified range of past NBA Games

import pickle
import pandas as pd

from createModel import getTrainingSet, createDataFrame
from configureCWD import setCurrentWorkingDirectory


# Exports game information for all games between specified time period to 'Data' Folder within project
# End date will not be included in range
# season must be in form 'yyyy-yy' and startDateOfSeason must be in form 'mm/dd/yyyy'
# filename must end in '.csv'
def getTrainingSetCSV(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startDateOfSeason, filename='gamesWithInfo.csv'):

    # Gets date, teams, and z-score difs for every game within range
    rangeOfGames = getTrainingSet(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startDateOfSeason)
    rangeOfGamesDataframe = createDataFrame(rangeOfGames)

    setCurrentWorkingDirectory('Data')

    rangeOfGamesDataframe.to_csv(filename)


# Creates a csv file that gives predictions for range of games
# Prints accuracy of model in predicting games for specified range
# gameDataFilename and outputFilename must be '.csv' files
def getPredictionsCSV(gameDataFilename, outputFilename):

    setCurrentWorkingDirectory('Data')

    gamesWithZScoreDifs = pd.read_csv(gameDataFilename)

    withoutNums = gamesWithZScoreDifs.loc[:, 'Home':'Date']  # Slices dataframe to only includes home through date
    justZScoreDifs = gamesWithZScoreDifs.loc[:, 'W_PCT':'TS_PCT']  # Slices dataframe to only include statistical differences

    setCurrentWorkingDirectory('SavedModels')
    with open('finalized_model.pkl', 'rb') as file:  # Change filename here if model is named differently
        pickleModel = pickle.load(file)

    predictions = pickleModel.predict(justZScoreDifs)  # Creates list of predicted winners and losers
    probPredictions = pickleModel.predict_proba(justZScoreDifs)  # Creates list of probabilities that home team wins

    numCorrect = 0
    numWrong = 0
    allGames = []

    for i in range(len(probPredictions)):

        winProbability = probPredictions[i][1]
        homeTeam = withoutNums.iloc[i, 0]
        awayTeam = withoutNums.iloc[i, 1]
        date = withoutNums.iloc[i, 10]

        currentGameWithPred = [date, homeTeam, awayTeam, winProbability]

        allGames.append(currentGameWithPred)

        # Creates dataframe that holds all games info and predictions
        predictionsDF = pd.DataFrame(
            allGames,
            columns=['Date', 'Home', 'Away', 'Home Team Win Probability']
        )

        setCurrentWorkingDirectory('Data')
        predictionsDF.to_csv(outputFilename)  # Saves game info with predictions in data folder as csv file

        value = withoutNums.iloc[i,9]
        if value == predictions[i]:
            numCorrect += 1
        else :
            numWrong += 1

    print('Accuracy:')
    print((numCorrect)/(numCorrect+numWrong))  # Prints accuracy of model in predicting games for specified range


# Generates probability predictions over specified range of games exports them to a csv with game info
# gameDataFilename and outputFilename must end in '.csv'
# season must be in form 'yyyy-yy' and startDateOfSeason must be in form 'mm/dd/yyyy'
def makePastPredictions(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startDateOfSeason,
                       gameDataFilename='gamesWithInfo.csv', outputFilename='predictions.csv'):

    # Obtains info for range of games
    getTrainingSetCSV(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startDateOfSeason,
                          gameDataFilename)
    # Makes probabilities for range of games
    getPredictionsCSV(gameDataFilename, outputFilename)


# start date (yyyy, m, d) (must be at least three days after start of season), end date (yyyy, m, d) (non-inclusive),
# season(yyyy-yy), start date of season (mm/dd/yyyy), .csv filename for games with z score differences,
# .csv filename for games with predictions
# EDIT THIS
makePastPredictions(2018, 12, 28, 2019, 1, 13, '2018-19', '10/16/2018',
                    'gamesWithInfo.csv', 'predictions.csv')

