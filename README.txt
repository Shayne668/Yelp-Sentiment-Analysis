# CSE6242-Team-52, README

## Important

Required: Python 3.10+
Caution: A recent update (as of November 26, 2023) to Macbooks with an M1 chip causes an error with the Flask application needed to generated word clouds with our Tableau Visualization. 
We do not know of a fix at the time, but all instructions below should still work for a Windows device or un-updated Macbook.

## Package

This project mainly utilizes the following Python packages (not going to cover their dependency):

- [pyspark]: Data preprocessing.
- [pandas]: Data preprocessing and ETL.
- [matplotlib]: Internal plotting and visualization used in both pre-processing and analysis.
- [tqdm]: Used for internal preprocessing to get an approximate time frame to finish a process.
- [statsmodels]: Time series analysis using ARIMA.
- [pmdarima]: ARIMA parameter tuning with auto_arima.
- [scikit-learn]: Perform train-test split, calculate mean squared error.
- [wordcloud]: Visualization of regular word clouds and polarity word clouds.
- [Flask]: Simple server setup that will return our word cloud visualizations.
- [Flask-Caching]: CSV caching to ensure that we don't need to re-read the csv file within 5 minutes for faster server response.
- [vaderSentiment]: Sentiment analysis package used to assign sentiment score for review, sentence, and word.
- [spaCy]: Sentiment analysis package used to generate Named Entity Recognition (NER), which was used to find aspects in a review. The aspect was later combine with vaderSentiment to create aspect sentiment score or polarity word clouds (based on aspect sentiment score and frequency)


## Description

This project is designed to forecast customer sentiment scores for businesses on Yelp in the states of Pennsylvania, Florida, and California to enhance customer experiences and improve business insights. 
A flowchart version of this project description is available inside the CODE folder as 6242_project_flowchart.svg.

PySpark was used on Amazon Athena to process the JSON-like data from the Yelp Open Dataset (https://www.yelp.com/dataset) into business information and reviews (https://www.yelp.com/dataset/documentation/main) from three states: 
Pennsylvania, Florida, and California. 

OpenRefine was used to cluster city and business names for sanitization. Python was used for sentiment scoring on these subsequent datasets in using VADER, and time series forecasting of future sentiment scores was performed using ARIMA. 

The expectation is that the user does not need to complete the processing steps for the raw data themselves, as the outputs of these scripts are formatted as comma-separated values (csv) available inside the data folder within CODE. 
If the user wishes to view the entire process, replicate, or expand on the project, the unedited processing scripts used in this project are provided inside the PROCESSING folder within CODE. 
Note/warning: File pathing and output names may be incorrect.

The interactive visualization component is a Tableau dashboard, available on Tableau Public, integrated with Flask in order to dynamically generate document-level word clouds and aspect-level polarity word clouds.
The workbook is available inside the CODE folder as 1122.twbx, and its corresponding data extract is StackedDataset.hyper inside of the data folder. 

Instructions for installation and setup are provided below. 
We strongly emphasize following the below instructions to interact with our visualization using Tableau Public + Flask, rather than trying to set up the workbook and its data sources locally because we cannot guarantee the latter's functionality.

## Demo Video Link
https://youtu.be/xwjVex-r9ig

## Installation

To get started, follow the steps below to install the required libraries:

1. Download the CODE folder where all project files are located in team52final.zip.

2. In a terminal, navigate to the directory where CODE was downloaded, e.g.
   ```
   C:/Users/username/Documents/team052final/CODE
   ```

3. Install Required Libraries:
    ```
    pip install -r requirements.txt
    ```
 
## Execution

Once the installation is complete, follow these steps to run the project:

1. Run the application:
    ```
    python run.py
    ```

This command will start the application and prepare it for use with Tableau. Leave it running while you continue to the next steps.

## Tableau Integration

To visualize the data in Tableau, follow these steps: 

1. Access Visualization on Tableau Public: https://public.tableau.com/app/profile/tony.ho6073/viz/1122_17006929023780/Dashboard1 
* High Level Overview of our visualization, might be slower due to limitation of Tableau public.

2. Navigate to Business Data:
    - Click on any “State” (blue) to zoom in to available business locations.
    - Hover one of the businesses and get a high level overview of the business in both aggregate performance and business customer sentiment performance compared to “similar business” in the same city.
    - Click on the business to see:
        - How the business performs based on customer reviews on document level.
        - How the business might perform on document level in the next time period (6 months later, currently not planning to forecast further).
        - How the business performs compared to similar business types within the same city.

3. Word Cloud Visualization:
Note: It may take several minutes to generate word clouds the first time you do it.
    - Require your local FLASK server running from the earlier run.py:
        - Get Word Cloud Image: Common word cloud of customer reviews based on frequency.
        - Get Polarity word clouds: Unique polarity word clouds that take advantage of NER aspect generation and Vader Sentiment scoring. Usual word cloud is simply scaled by frequency, the polarity word clouds generated from here is based on the Vader sentiment score (-1 ~ 1) and its frequency for three main different category (Person, Product, Organization) 
