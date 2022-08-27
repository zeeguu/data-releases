# The Zeeguu Database Dumps

## Contents
- [About](#about)
- [Importing the Data from the Command Line](#importing-the-data-from-the-command-line)
- [Running Python Analyses](#running-python-analyses)
- [Versions](#versions)
- [Database Description](#database-description)

## About

Here we publish and plan to store MySQL dumps from the Zeeguu project. 

## Importing the Data from the Command Line

[on a Linux or Mac] Clone this repository. Then from within the Data-Releases folder, run the following: 
````
unzip zeeguu_anonymized-2021-01-06.sql.zip
mysql -uroot -p -h localhost zeeguu_test < zeeguu_anonymized-2021-01-06.sql
````

Once the database is imported in MySQL DB server you can run queries on the database. Example SQL queries are available [in the Zeeguu-API repository](https://github.com/zeeguu-ecosystem/zeeguu-api/tree/master/tools/sql)



## Running Python Analyses

To analyze the data from Python see [PYTHON_ANALYSIS.md](./PYTHON_ANALYSIS.md). 


## Versions

#### 2022-06-04
* 648 active users since 2021
* 1368 active userse since 2016


#### 2021-01-06

* 497 users active in more than 10 distinct days in 2021
* 1097 users active in more than 10 distinct days since 2016
* removed anonymous accounts
* special user ids: 
	* 534 - dev - used with multiple languages (learning mainly german)
	* 2953 - dev - learning mainly danish
* there seems to be a bug where TRANSLATE TEXT does not have the translated text for more recent entries; this should not be a problem because the information should be retrievable from the bookmark table





## Database Description

* **user** - info about a user 
* **article** - info about an article, including fk_difficulty - the difficulty that's presented in the UI; language 
* **bookmark** - a word or group of words that has been translated by a user in an article together with the time when it was translated
* **user\_activity\_data** - logs events relevant for understanding users interaction with texts and exercises (and the platform in general)
	* interactions in the article reader are prefixed with UMR (e.g. UMR - TRANSLATE TEXT);

* **user\_reading\_session** - this is our attempt at inferring the time spent while reading an article; the current implementation takes as input events that suggest [user interactions](https://github.com/zeeguu-ecosystem/zeeguu-api/blob/master/zeeguu/core/model/user_reading_session.py) with the article (article open, translation, speech, scroll, mouse move, etc.) and as long as the user is active, considers the user involved in a **reading session**. There is a timeout of 2min: if the user did not interact with the article in the reader for 2min, the session is closed; thus, this is more precise that considering *reading time = timestamp closed - timestamp opened* but now one must stitch together multiple reading sessions to figure out something like [reading macro sessions](https://github.com/zeeguu-ecosystem/DB-Examples/blob/master/python-analysis/macro_session.py) that can be used in estimating the actual reading time for an article. 

* **user\_exercise\_session** - same as reading session, but computed for exercises




