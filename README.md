# README for Zillow Clustering Project

<hr style="border-top: 10px groove #1277e1; margin-top: 1px; margin-bottom: 1px"></hr>

## Project Goals and Ideas
### The Big Question: What is driving the errors in the Zestimates?

For this project the target is `logerror`

#### Goal: Identify Drivers of Error and Create model(s) that account for those drivers.

#### Initial Thoughts and Hypotheses
- After only looking at size (bedroom count, bathroom count and square footage for the house itself) model was not great
- Location is very important in real estate. As they say Location Location Location
    - Use Latitude and Longitude to narrow down groups
    - Create clusters of error based on location
    - if that doesn't work, try to use location data and price to create neighborhood clusters  
- Price per square foot is something lots of realtors use for comparing houses that aren't the same size 
    - Create engineered feature, `ppsqft` divide `taxvalue` / `calculatedsquarefeet` 
- Age of home is important when comparing houses, realtors will compare houses built before 1978, between 1798-2000 and post 2000
    - Create engineered feature age, based on year built
    - Create three bins
- Related to size of home, homes typically get compared with other homes within a 400sqft variance. Possibility here to create size clusters based on `calculatedsquarefeet`, or `ppsft`, or `lotsize`

<hr style="border-top: 10px groove #1277e1; margin-top: 1px; margin-bottom: 1px"></hr>

## About the Data
- The data in this project comes from the Zillow data prize competition in 2017.

### Data Dictionary

<hr style="border-top: 10px groove #1277e1; margin-top: 1px; margin-bottom: 1px"></hr>

## Plan and Process
- Trello Board (insert link here)
- Outline 
- 

## How to recreate this project

You will need your own env file with database credentials along with all the necessary files listed below to run my final project notebook.

1. Read the README.md
2. Download the wrangle.py, evaluate.py, explore.py and final_notebook.ipynb files into your working directory, or clone this repository 
3. Add your own env file to your directory. (user, password, host)
4. Run the final_notebook.ipynb notebook

### Skills Required
Technical Skills
- Python
    - Pandas
    - Seaborn
    - Matplotlib
    - Numpy 
    - Sklearn

- SQL

- Statistical Analysis
    - Descriptive Stats
    - Hypothesis Testing
    - T-test
    - Chi^2 Test

- Regression Modeling
    - Linear Regression Evaluation Methods
        - RMSE, R2, etc
    - Tweedie Regressor
    - Lasso Lars
