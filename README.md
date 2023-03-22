# CEL

Hi I'm Mei <3

This is my submited project for Data Engineer position at CEL consulting. The goal is to build a web app that will allow to showcase the results of data analysis of this raw data, then also allow users to explore stock data of related companies.

On using technology that will be close to what we are using at CEL for data engineering and dev: Pandas, Streamlit and FastAPI.

## 1. How to run it

- Clone source code from github

    ```
    git clone https://github.com/uyen-pp/simcel.git
    ```
- Run with docker compose 

    ```
    cd simcel
    docker compose build
    docker compose up
    ```

    After all done you can now view Streamlit app in browser on: http://0.0.0.0:10001


## 2. What will you see

The app includes 4 tabs from those you can see: 

1. CEL Data: 
    - To show *cleaned* CEL data. Raw data is cleaned and missing values are filled in by reasonable values. Some caterical labels like *'Low Fat'*, *'low fat'*, *'LF'* are converted to be the same value (*'Low Fat'*), etc 
    - Data is also separated into 3 tables `Items`, `Outlets` and `Sales`, that is to be conformity with database design standards.

    All the works done in this file: 
    
    ```simcel/exploration/data_processing.ipynb```

2. CEL Exploration
    - This is to conduct minimal data exploration analysis, i.e try to understand some of the variable relationships in the dataset.
    - The app also allow user interaction, that is, user can choose which attributes to show in the chart.

3. YFIN Chart
    - To create a stock charts for any ticker symbol or name that user types in. And then a chart will be presented to them where they can modify the time intervals. It should look something like the image below (using paypal as reference).
    
    - `yfinance` is used to get stock data. Other resouces that is found on the internet to provide company's information also bi used.

    - There is a button checkbox here let users add the current ticker to there favorite list.

4. Favorites (Saved):

    - All favorite tickers data should be shown on the chart at the same time to be able to compare them and select which one to buy.

    - User now can hide/unhide any line by unchecking/checking at the corresponding checkboxs.

## 3. Project overview

The file systems:

- Cel (cel service): provide CEL's data through FastAPI.

- YFin (yfin service): provide stock data through FasAPI

- UI: Streamlit app works as Frontend

- exporation: data preprocessing and analysis

For each service I build an individual image, all to be run by docker-compose.

## 4. My feedback

The data: As far as i understand, there may be some points that are not correct in the data description, such as: 

- Item_Visiability, Item_Outlet_Sales, Outlet_Establish_Year should not be Nominal,

- Categorical variables: Item_Fat_Content, Item_Type, Outlet_Size, Outlet_Location_Type, Outlet_type,

- Continous variables: Item_Weight, Item_Visability, Item_MRP, Item_Outlet_Sale, Outlet_Establish_year,

These made me a litle bit concerned.

The time:

- It took me 4hours/day for 4 days working on the project, there are lots of thing to do. (Hope that doesn't exceed the time limit !)

- Streamlit is great but since it is not really a front-end frameworks, I had to work on it quite a bit, to make everything do as expected.

*** Thank you for reading ***
