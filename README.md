# The script provides studies about API requests.

## Raw data from Police Department Incident Reports

> more details in: https://dev.socrata.com/foundry/data.sfgov.org/wg3w-h783

## Architecture

- I'm using Python as language and Cloud Platforms like Google Cloud and Azure
- Basically, I'm requesting data from API and storage it on Cloud Storage (Phase 1 and 2) :::**DONE**::: 
- Then in the Phase 3 I'll start developing on Azure Plarform using the medallion architecture :::**DOING**:::
- The data layers will be Bronze :::**DONE**::: > Silver :::**DOING**::: > Gold :::**TO DO**:::

## Ideas behind the scenes

> more details in: https://www.ibm.com/garage/method/practices/code/construct-data-topology/ and
> https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion

## The Raw ingestion using Python Functional Programming best practices: phase 1

> request_socrata_soda.py ingest data from Police Department Incident Reports in a JSON form and load into a bucket using parameters to define the start incident_datetime and the number_of_days desired. The idea is for testing the processing and reprocessing feature.

> extract_load_data(bucket_name=YOUR BUCKET NAME, start_date=start_date, number_of_days=DESIRED integer) is the function that you'll use to run this code and in the line 15 to 19 there's some static variables to play with.

> to run this code you'll need to provide a config.json that wasn't provided here. If you want to run, just clone and follow this dictionary:

```
{
    "api":{
        "domain": {
            "url": "https://data.sfgov.org/resource/"
        },
        "dataset": {
            "san_francisco_data": "wg3w-h783"
        },
        "credentials": {
            "username": "<YOUR CREDENTIAL>",
            "password": "<YOUR PASSWORD>"
        },
        "headers": {
            "X-App-Token": "Ax7ks1Cmr0r6TEssy44yJj4ts",
            "Content-type": "application/json"
        },
        "params":{
            "$limit": "9999999999", 
            "$where": "incident_datetime",
            "$$exclude_system_fields": false
            }
    },
    "gcp":{
        "credentials":{
            "folder": "<YOUR JSON FOLDER>"
        },
        "bucket": {
            "mode": "socrata",
            "bucket_name": "<YOUR BUCKET NAME>",
            "prefix_socrata": "socrata",
            "prefix_test": "test"
        }
    }
}
```

> to get the credentials for data extraction visit https://dev.socrata.com/docs/endpoints.html and follow the instructions.

> to get credentials for data storage visit https://cloud.google.com/free?hl=pt-br and follow the instructions.

> in the files folder you'll see files from this code in csv and JSON format. Use the socrata_2018-01-01_dataset_wg3w-h783_crimes_in_loaded_1682068024187410300.json to see the results, because the others are only test.

> in the guidance folder you'll see studies from Corey Shaffer channel on https://youtu.be/tb8gHvYlCFs.

> in the trials folder you'll see some free coding.

> this codes has many to dos, so do not hesitate in criticize. Although, I'll not provide any update on it, just learn from your thoughts.

## The Raw ingestion using Python best practices: classes - phase 2

> in this phase I'll study and implement classes to organize and make this code more readable, reusable and scalable :::**DONE**:::

> My thoughts about the classes diagram looks like:

```
utils.py
    Utils
        modify_entry_params()
        logger

socrata.py
    Params
    Socrata
	    api_connection()
		logger

storage.py
    Client
        client_storage()
        logger
    Bucket
        bucket_obj()
        logger
    Blob
        list_blobs() 
		logger
    Blob_obj
        blob_obj()
        logger

data_ingestion.py
    Data
        list_dates()
        ingestion()
        logger
main.py 
```
## The development of medallion architecture in Azure Platform - phase 3

### 01-raw

This parameterized template developed here ingest raw data from the City and County of San Francisco using Socrata Open Data API. The San Francisco Police Department's (SFPD) Incident Report Dataset is one of the most used reports for crime analysis. See the literature [here](https://www.sanfranciscopolice.org/sites/default/files/2022-11/SFPDQADRReport-2ndQuarter-20221129.pdf) and [here](https://scholar.google.com.br/scholar?hl=pt-BR&as_sdt=0%2C5&q=The+San+Francisco+Police+Department%E2%80%99s+%28SFPD%29+Incident+Report+Dataset&btnG=).

The holistic workflow presented below executes everyday at 11AM UTC, flag the trigger time as a watermark and store it in the /execution_logs/01-raw/ingestion_api_socrata.log. Then, the next execution starts from the last execution time in the log. This techinique is well documented [here](https://dwbi1.wordpress.com/2022/05/22/watermark-in-data-warehousing/) and [here](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-overview). 

Bronze Layer

![](/phase_3/images/bronze_layer.png)

The response from Socrata API is a JSON format and is stored in a hierarchical structure inside the blob storage Gen2 like Year/Month/watermakUnixTimestamp_fieldName_reportGenerationYYYMMDD.json

Hierarchical Structure in the blob Storage Gen2

![](/phase_3/images/bronze_hierarchical_structure.png)

### 02-silver

This parameterized template fetch the data after 10 minutes of the bronze layer pipeline execution, applies the watermark technique storage and writes it in a new column. Then the data is converted to parquet and snappy compressed. The holistic workflow is presented below:

Silver Layer

![](/phase_3/images/silver_layer.png)

Hierarchical Structure in the blob Storage Gen2

![](/phase_3/images/silver_hierarchical_structure.png)

In the silver layer the data has to be validated, enriched and ready for downstream analytics. Data profiling technique was applied using python and pandas library to understand the data types and data patterns for the data quality improvements. The scenario described below shows the evaluation steps that leads to the mapping phase in the pipeline and for the transformations needed to make data available in the right way:

Data profiling ::: DEV :::

The parameters for data analysis ranges from 1 March 2022 until 31 March 2023. The data shape has 149.272 records per 31 columns (20% coverage of total size 735.432).

Missing values

The transformations

![](/phase_3/images/silver_data_profiling_missing.png)

