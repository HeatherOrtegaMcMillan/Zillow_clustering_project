# README for Zillow Clustering Project

<hr style="border-top: 10px groove #1277e1; margin-top: 1px; margin-bottom: 1px"></hr>

## Project Goals and Ideas
### The Big Question: What is driving the errors in the Zestimates?

For this project the target is `logerror`. I have an engineered feature called `abs_logerror` that is the absolute value of the logerror. 

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

| **Column Name**                | **Description**                                                                                                             | **Use**                             |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| `parcelid`                     | Unique Identifier for each property                                                                                         | Identifier                          |
| `logerror`                     | The calculated amount the original Zestimate model missed guessing the home value by. Came straight from database.          | Target (after being transformed)    |
| `abs_logerror`                 | Absolute value of logerror. Calculated for this project.                                                                    | Target                              |
| `bathroomcnt`                  | Number of bathrooms                                                                                                         | Variable (continuous)               |
| `bedroomcnt`                   | Number of bedrooms                                                                                                          | Variable (continuous)               |
| `calculatedfinishedsquarefeet` | Total Square footage of home. Original column name calculatedfinishedsquarefeet.                                            | Variable (continuous)               |
| `ppsqft`                       | Price Per Square foot. Calculated using `calculatedfinishedsquarefeet` and `taxvaluedollarcnt`                              | Variable (continuous)               |
| `latitude`                     | Latitude location of property.                                                                                              | Variable (continuous)               |
| `longitude`                    | Longitude location of property                                                                                              | Variable (continuous)               |
| `tax_amount`                   | Amount of tax collected for property                                                                                        | Information                         |
| `fips`                         | Federal Information Processing Standards Code. Indicator of county.                                                         | Information                         |
| `county`                       | County where the property is located. Generated from `fips`                                                                 | Information                         |
| `taxamount`                    | Amount of property taxes paid for property.                                                                                 | Variable (continuous)               |
| `taxvaluedollarcnt`            | Tax appraised value of home. Original column name taxvaluedollaramount.                                                     | Variable (continuous)               |
| `tax_rate`                     | Percentage of value that was paid in taxes. Calculated from `taxvaluedollarcnt` and `taxamount`                             | Variable (continuous)               |
| `yearbuilt`                    | Year the house was built                                                                                                    | Variable (continuous)               |
| `age`                          | How old the house is in years (in 2017). Calculated from `yearbuilt`                                                        | Variable (continuous)               |
| `yearbuilt_bins`               | Created bins indicating whether the house was built before 1978, between 1978 - 2000, or after 2000.                        | Variable (categorical)              |
| `propertycountylandusecode`    | Shows code used by county for the use of the land.                                                                          | Information                         |
| `propertylandusetypeid`        | ID used to show what type of home it is (single family, mobile home, etc.)                                                  | Information                         |
| `propertylandusedesc`          | Actual description of `propertylandusetypeid` to show what type of home was on the property (i.e. 261 = Single Family Home) | Information, variable (categorical) |
| `rawcensustractandblock`       | Square footage of property as a string. Not used. See `calculatedfinishedsquarefeet`                                        | Information                         |
| `structuretaxvaluedollarcnt`   | Square footage of structure on property.                                                                                    | Information                         |
| `landtaxvaluedollarcnt`        | Square footage of land on the property.                                                                                     | Variable (continuous)               |
| `transactiondate`              | Date home was sold.                                                                                                         | Variable (continuous) / Information |


<hr style="border-top: 10px groove #1277e1; margin-top: 1px; margin-bottom: 1px"></hr>

## Plan and Process
- Trello Board (insert link here)
- Outline 
- 

### Process

✅ **Plan** -> Acquire -> Prepare -> Explore -> Model & Evaluate -> Deliver
- Read over project requirements and lay out basic plan
- Create [Trello board](https://trello.com/b/9EmzDpkc/zillow-clustering-project)
- Outline Story for Presentation
- Think about and establish overarching question that needed to be answered
- Look at other work I had done with the Zillow Dataset to see what I alreayd had

Plan -> ✅ **Acquire** -> Prepare -> Explore -> Model & Evaluate -> Deliver
- Since I already had some work with Zillow dataset under my belt, I tweaked the acquire
function that I already had to ensure I had the all the data I would need
- Took a look at all the rows and columns I had pulled to a jupyter notebook
- Here is where I took care of ensuring I had the following:
    - Transaction date in 2017
    - Unique properties with only their most recent transaction date
    - Latitude and longitude were not blank
- There were a total of 77380 rows, 46 columns to start

Plan -> Acquire -> ✅ **Prepare** -> Explore -> Model & Evaluate -> Deliver
- In the prepare phase the biggest challenge was taking care of Nulls and outliers and deciding what to do about them
- This step is where I filtered for single family homes 
    - For the scope of this project that includes all homes marked as: 'Single Family Residential', 'Townhouse', 'Manufactured, Modular, Prefabricated Homes', 'Mobile Home'
- Dropped columns missing too much data
- Dropped rows missing too much data
- Created new features to better help understand data
    - create `age` and `yearbuilt_bins`
    - create `ppsqft` 
    - create `county` column from `fips`
    - create `taxrate`
    - create `abs_logerror` from `logerror`
- I also dropped outliers here. For this project I dropped homes that had:
    - A tax rate higher than 15%
    - A bathroom count higher than 6 or lower than 1
    - A bedroom count higher than 7 or lower than 1
- With more time I would like to revisit dropping outliers to see if I can create better models and clusters
- I came back to prepare several times during the pipeline, to prune the data a little more for whatever step I was on. Because of this, in the wrangle file you will see two wrangle functions. This is the reason why. 

Plan -> Acquire -> Prepare -> ✅ **Explore** -> Model & Evaluate -> Deliver
- First step was to see the distributions of all variables and my target
- It was during the explore phase that I realized I needed to create `abs_logerror`
    - This was to make it easier to comprehend where the model was messing up. I decided not to 
    care about if it was guessing high or low, just how far off
- In Bivariate exploration (after splitting my data), I plotted all variables against the target to see if any drivers or clusters jumped out at me. They didn't. 
- Biggest takeaway was **The estimate had the largest error on smaller and cheaper homes**

Explore --> **Clustering** --> Statistical Testing
    - I decided to create clusters based on location (since location is important in real estate) and age, and location and price
    - I experimented with several clusters using latitude, longitude, age and ppsqft. Adjusting the k value and visualizing as I went
    - With more time I'd like to optimize this step. Perhaps creating clusters on size and age of the home as well 
    - Ultimately I ended up using my clusters based on location and price in the modeling phase
        - I saw from box plots that cluster 6 might have some value as the mean abs_logerror looked slightly different than the other clusters

Explore --> Clustering --> **Statistical Testing**
- To get started before running some statistical tests, I created a heatmap to see some general correlation between my variables, my cluster groups and my target
    - I completed some one hot encoding of my categorical variables before this 
    - I also scaled my data using a Min Max Scaler 
- I looked at the relationship between age and absolute logerror, in several ways (using the yearbuilt bins and using the continuous variable age)
- I looked at whether cluster 6's mean absolute log error different from the population as a whole
- For more details on my statistical testing see my Final Notebook(PUT LINK HERE)

Plan -> Acquire -> Prepare -> Explore -> ✅ **Model & Evaluate** -> Deliver
- I decided, because the distribution of the target (logerror) was normal-ish, to use OLM and Lasso Lars models 
- The baseline is predicting the mean absolute log error
- Set out to create two sets of models
    - Try a generic model with my clusters and features included
        - Is it better than the baseline? - YES by 0.001 (RMSE) on seen and unseen data
    - Try groupings of models based on age by dividing data up (old and new houses) and creating separate models for each
        - Do these models perform better than the baseline? Or better than the generic model from before? - They do perform better than baseline, but not notably better than the first models. Also, they were kind of a pain to make.


Plan -> Acquire -> Prepare -> Explore -> Model & Evaluate -> ✅ **Deliver**
- The final notebook was created for the walk through presentation and is structured for that purpose
- This README was fleshed out extensively
- All modules used are located in this repo

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

- Clustering
    - k Means and inertia