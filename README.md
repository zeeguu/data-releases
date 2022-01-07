# Anonymized Database Dumps


* from the Zeeguu project
* in SQL format

## Version Details

### 2021-01-06

* 497 users active in more than 10 distinct days in 2021
* 1097 users active in more than 10 distinct days since 2016
* removed anonymous accounts
* special user ids: 
	* 534 - dev - used with multiple languages (learning mainly german)
	* 2953 - dev - learning mainly danish
* there seems to be a bug where TRANSLATE TEXT does not have the translated text for more recent entries; this should not be a problem because the information should be retrievable from the bookmark table


## Main tables

* **user** - info about a user 
* **article** - info about an article, including fk_difficulty - the difficulty that's presented in the UI; language 
* **bookmark** - a word or group of words that has been translated by a user in an article together with the time when it was translated
* **user\_activity\_data** - logs events relevant for understanding users interaction with texts and exercises (and the platform in general)
	* interactions in the article reader are prefixed with UMR (e.g. UMR - TRANSLATE TEXT);

* **user\_reading\_session** - duration of a continuous interaction wit the reader; duration is in ms; sessions are closed if a user does not interact with a text for 2min
* **user\_exercise\_session** - same as reading session, but computed for exercises


## How to use

* Import to a local MySQL DB, and run queries on it. Some example SQL queries are available [in the Zeeguu-API repository](https://github.com/zeeguu-ecosystem/zeeguu-api/tree/master/tools/sql)
* To analyze the data from Python using the `zeeguu.core.model` [API](https://github.com/zeeguu-ecosystem/zeeguu-api/tree/master/zeeguu/core/model) see [PYTHON_README.md](./PYTHON_README.md). 





