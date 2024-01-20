# The Guardian News Scraping

## Introduction
In this project, we will be using an application to crawl the online news on website [The Guardian](www.theguardian.com/au) using a crawler framework called [Scrapy](http://scrapy.org/). Here are the tools that we will be using:
- Python - Scraping data from [The Guardian](www.theguardian.com/au) Store the data in BigQuery 
- BigQuery - Our datawarehouse wherein  will be stored into and queried from
- Flask - Creates an API that provides access to BigQuery database content and allows to search for articles by keyword
- Power BI - Enables the visualization of a dashboard for user interaction with Bigquery data

![WORKFLOW](https://github.com/csonicholas/ASSETS/assets/108910737/dfd26d1d-7d59-4b29-ac4d-50a03e652799)


## Project Files
- Scrapy
    - news_spider.py - Our main that scrapes articles from www.theguardian.com/au and then sends the extracted data to Google BigQuery.
    - scrapy.cfg - deploy configuration file
    - items.py - project items definition file
    - middlewares.py - project middlewares file
    - pipelines.py - project pipelines file
    - settings.py - project settings file
    - spiders/ - a directory where you'll later put your spiders
            
    
- Flask
    - app.py - Contains the logic for creating the Api and extracting data from bigquery based on the desired keyword
 

## Workflow


Let's break this down into the following main steps.
- Configure credentials
- How to Create a new Scrapy Project
- Get The Guardian News Data
- Create API
- Data Visualization


## Configure credentials 

- Create a free account in [Google Cloud Plataform (GCP)](https://cloud.google.com/free)
- Click [here](https://developers.google.com/identity/protocols/oauth2/service-account?hl=en) to learn how to generate service-account credentials.
- With the json file, set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
``` 
export GOOGLE_APPLICATION_CREDENTIALS="path/key.json"
```


## How to Create a new Scrapy Project
- Change to the project folder directory.
- Open a terminal and create a Python virtual environment using:

``` 
Windows
python -m venv venv

Mac/Linux
python3 -m venv venv
```
Then activate it by executing


``` 
Windows
venv\Scripts\activate

Mac/Linux
source venv/bin/activate

```

- Install Scrapy using:
``` 
pip install Scrapy
```


- See [Scrapy documentation](www.docs.scrapy.org/en/latest/intro/install) to more informations.

- To start a new Scrapy Project called news, run:

``` 
scrapy startproject news
```


## Get The Guardian News Data

-  Change to the new directory, generate a new spider and the website desired :

``` 
cd news

scrapy genspider news_spider https://www.theguardian.com/au
```

- A new file called news_spider.py will be created. To run this file:
```
scrapy crawl news_spider
```

- Note: Replace the variables 'dataset_id' and 'table_id' in the code for your own dataset and table_id.

- The data will be extracted and sent to BigQueryuery.

![GoogleBigQuery](https://github.com/csonicholas/ASSETS/assets/108910737/882ef12b-b344-430e-8bc5-bff2decd2f92)



## Create API

- The Flask framework was used.
- The API provides access to the content in BigQuery database to search for articles by a keyword.

![news_postman](https://github.com/csonicholas/ASSETS/assets/108910737/fe0b6d0b-e29a-4f69-b966-4f8c9218fb28)

- The endpoint is 'api/search?keyword={keyword}' e.g api/search?keyword=music


## Data Visualization




This dashboard made in Power BI was created as a way to demonstrate some of the applications of the data. [Click here to view](https://app.powerbi.com/view?r=eyJrIjoiNDU2MTI0M2MtNmVhMS00ODY3LTg5ODQtOGNhMjY0MDMzN2FmIiwidCI6IjhjMjRmYmZiLWEzNGQtNGI3Yy1iZDEzLTEzMWEwMmIyNGUzNSJ9).


