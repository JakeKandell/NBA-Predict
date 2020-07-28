# NBA-Predict <img align="right" width="75" height="155" src="https://cdn.freebiesupply.com/images/large/2x/nba-logo-transparent.png">


Predicts NBA Games Using a Logistic Regression Model in Python

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

### **Installation**

```bash
pip3 install -r requirements.txt
```

### **Daily Predictions**
1. Open nbaPredict.py
2. Edit the call to makeInterpretPrediction with desired date of games, season, and the start date of the season
![NBA-Predict Image](https://user-images.githubusercontent.com/24983943/71434218-7e677e00-26b1-11ea-8a20-cad8d410b251.png)
3. Run the program either through the terminal or an IDE
4. Wait ~1-3 minutes for model to finish scraping stats and predicting outcomes
5. Outcomes are outputted as the percent chance that the home team will defeat the away team
![Screen Shot 2019-08-01 at 5 41 22 PM](https://user-images.githubusercontent.com/24983943/62329326-9977ee00-b483-11e9-9ce3-b9c9cdf78938.png)

### **Past Predictions**
1. Open makePastPredictions.py
2. Edit the call to makePastPredictions with desired start date, end date, season, start date of the season, and output
filenames. NOTE: The start date should be at least three days after the season begins and the end date is non-inclusive.

    ![Screen Shot 2019-10-11 at 1 41 42 AM](https://user-images.githubusercontent.com/24983943/66627069-7f1b6880-ebc8-11e9-9a94-981b2fa61f1e.png)
3. Run the program either through the terminal or an IDE
4. Two CSV files will be saved in the Data folder. One holds the gameData and the other holds the predictions for the games. The time to execute will vary greatly from a couple minutes to a several hours depending on the range between the start and end date.


# Accuracy Information
### **Confusion Matrix**

![rsz_1confusionmatrix](https://user-images.githubusercontent.com/24983943/71774907-20565880-2f45-11ea-85c2-a4073a0ac7df.png)

**Accuracy: 0.7037 (532/756)**

**Precision: 0.7367 (375/509)**

**Recall: 0.8065 (375/465)**
