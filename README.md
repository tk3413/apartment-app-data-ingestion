# Apartment App Data Ingestion

## Purpose of this repo
To scrape apartment data from websites

## The bigger picture
To warehouse apartment data for analysis

## Layout
Each of the directories in this repository is an independent data scraping module. Each independent module structure is as follows in this example:

- vita
    - vita.py <- scraper logic 
    - requirements.txt <- contains python libraries necessary for execution
    - Dockerfile <- required for deployment to cluster for automated ingestion
    - Makefile <- [optional] for Mac users only, but pretty helpful

## To add a new scraper
- Copy the existing `vita` directory with a one-word name for the new apt complex you wish to add
```
    cd data-ingestion
    mkdir monkeys
    cp -r vita/ monkeys
```
- Rename the python file
```
    cd data-ingestion
    mv monkeys/di-vita.py monkeys/di-monkeys.py
```
- Rename line `5`  of the Dockerfile from `vita` to `monkeys`.
- Rename line `11` of the Dockerfile from `vita` to `monkeys`.
- Rename line `2`  of the Makefile (APPNAME) from `di-vita` to `di-monkeys` 
- Rename line `1`  of the Makefile (DOCKERUSERNAME) to your own Docker repo username
- Update `monkeys.py` to scrape the required data