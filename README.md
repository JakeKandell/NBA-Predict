# NBA-Predict
Predicts Daily NBA Games Using a Logistic Regression Model in Python

# Model
The model uses eight factors scraped from stats.nba.com to determine the predicted result of an NBA game. Each stat is adjusted to per 100 possessions to ensure pace has no impact on the predictions.

* Home Team
* Win Percentage
* Rebounds
* Turnovers
* Plus Minus
* Offensive Rating
* Defensive Rating
* True Shooting Percentage

# Usage
### **Daily Predictions**
1. Open nbaPredict.py
2. Edit the call to makeInterpretPrediction with desired date of games, season, and the start date of the season
![Screen Shot 2019-08-01 at 5 38 46 PM](https://user-images.githubusercontent.com/24983943/62329254-5f0e5100-b483-11e9-8bf9-21db5a0574bb.png)
3. Wait ~1-3 minutes for model to finish scraping stats and predicting outcomes
4. Outcomes are outputted as the percent chance that the home team will defeat the away team
![Screen Shot 2019-08-01 at 5 41 22 PM](https://user-images.githubusercontent.com/24983943/62329326-9977ee00-b483-11e9-9ce3-b9c9cdf78938.png)

### **Past Predictions**
1. Open makePastPredictions.py
2. Call makePastPredictions with desired start date, end date, season, start date of the season, and filenames
3. Two CSV files will be saved in the Data folder. One holds the gameData and the other holds the predictions for the games. The time to execute will vary greatly from a couple minutes to a several hours depending on the range between the start and end date.
 

# Accuracy Information
### **Confusion Matrix**
  
![ConfusionMatrixSmaller](https://user-images.githubusercontent.com/24983943/63641839-c8e4d980-c682-11e9-8c5d-cf04a650e814.png)

**Accuracy: 0.73134 (245/335)** 

**Precision: 0.75463**

**Recall: 0.815**
