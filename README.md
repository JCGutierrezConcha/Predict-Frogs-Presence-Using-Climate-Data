# Predict-Frogs-Presence-Using-Climate-Data

## Problem description

This project is based on 2022 EY Open Science Data Challenge: Biodiversity.

I worked in novice level of the challenge. In this level the task was to build a computational model that can identify the occurrence of frogs for a single location using a single data source.

Especifically I developed a species distribution model for litoria fallax across Australia using weather data from the TerraClimate dataset.

The dataset used in this project (`frogs_climate_data.csv`) was prepared using data between 1980 and 2019 and following features:

- aet (Actual Evapotranspiration, monthly total), units = mm
- def (Climate Water Deficit, monthly total), units = mm
- pet (Potential evapotranspiration, monthly total), units = mm
- ppt (Precipitation, monthly total), units = mm
- q (Runoff, monthly total), units = mm
- soil (Soil Moisture, total column - at end of month), units = mm
- srad (Downward surface shortwave radiation), units = W/m2
- swe (Snow water equivalent - at end of month), units = mm
- tmax (Max Temperature, average for month), units = Celsius
- tmin (Min Temperature, average for month), units = Celsius
- vap (Vapor pressure, average for month), units  = kPa
- ws (Wind speed, average for month), units = m/s
- vpd (Vapor Pressure Deficit, average for month), units = kpa
- pdsi (Palmer Drought Severity Index, at end of month), units = unitless

For each feature, the mean was calculated in the period analyzed (1980-2019).
That is why the suffix '_mean' was added to the name of each feature.

The target variable is ocurrenceStatus.
The presence of frogs is represented with a value = 1 and the absence with a value = 0.


## EDA

We conducted an Exploratory Data Analysis (EDA) to gain insights into our dataset. 

- We analyze distribution of target variable and features.

We transform 3 features (q_mean, ppt_mean and vpd_mean) because they are right-skewed, we will transform these features by function np.log1p

We eliminate 1 feature (swe_mean) because has 97.8% of a single value.

- We created a correlation matrix to analyze the relationships between numerical variables.

Since the correlation values between any two variables is not greater than 90%, none of the attributes were removed.


## Model Training

We trained following models:

- Random Forest Classifier
- Extra Trees Classifier
- XGBoost Classifier

We used k-fold cross-validation to assess model performance, and the average ROC AUC score was used as a metric.

## Tuning Models

For Random Forest hyperparameters tuned included the number of estimators, maximum depth and min_samples_leaf.

For Extra Trees hyperparameters tuned included number of estimators, maximum depth and min_samples_leaf.

-For XGBoost hyperparameters tuned included number of estimators, maximum depth and learning rate (eta).

We trained and evaluated the models on the validation dataset.


## Select Best Model

To choose the final model, we will train the tuned models with data from full train dataset and evaluate their performance with test dataset.

We selected the model with high ROC_AUC score, which is Random Forest.


## Exporting notebook to script

The logic for training the best model is exported to a separate script named `train.py`.


## Installation

First of all clone this repo 
```
git clone https://github.com/JCGutierrezConcha/Predict-Frogs-Presence-Using-Climate-Data.git
```

## Run with Docker

Once you have cloned the repo, you need to have Docker installed on your machine and just build and run the docker image.

To build the image run
```
docker build -t {build-tag} .
```
`{build-tag}`: Specifies any user-defined tag for docker image. eg. `app-test`


To run the image run
```
docker run -it --rm -p 9696:9696 {build-tag}
```

- -it enables an interactive terminal.
- --rm removes the container when it exits.
- -p 9696:9696 maps port 9696 on your host to port 9696 within the container.


## Usage app to predict

Open a new terminal, be sure requests is installed. If is necessary use ```pip install requests```.

Then run  ```python predict-test.py```.


## Sample Output

![Sample of the project running locally](https://github.com/JCGutierrezConcha/Predict-Frogs-Presence-Using-Climate-Data/blob/main/deploy_predict.PNG)


