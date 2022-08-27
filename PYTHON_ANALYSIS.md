## How to Run Analysis Scripts in Python

This has been tested on OS X but should work on Linux too. It requires you to have a local MySQL DBMS in which to import the DB dump in this repo. It also requires Python 3.6+ 




1. Clone this repo 

	- Import the DB into a local MySQL db
	- If you name the DB `zeeguu_test` and create a user `zeeguu_test` with the password `zeeguu_test` then you won't have to change any configuration later 

1. Change to the `/python-analysis` folder 

    ``` 
    cd python-analysis
    ``` 

1. Create a new virtual environment for zeeguu and activate it

    ``` 
    python3 -m venv zeeguu_env
    source zeeguu_env/bin/activate
    ```
    

1. Clone the zeeguu codebase and install requirements; then install the zeeguu package; this makes importing and using zeeguu related modules possible

    ```
    git clone https://github.com/zeeguu-ecosystem/zeeguu-api
    cd zeeguu-api
    pip install -r requirements.txt
    python setup.py develop
    ```

1. [Conditional] If you installed the DB with different credentials as mentioned above at point 1 then modify the MySQL connection string in  `zeeguu-api/default_api.cfg` accordingly. The connection string is: 

    ```
    "mysql://<user>:<pass>@127.0.0.1/<dbname>"
    ```

1. Export the ZEEGUU_CONFIG envvar like below: 

    ````
    export ZEEGUU_CONFIG=./zeeguu-api/default_api.cfg
    ````


1. Change to the `/python-analysis` folder and test that some of the simple analyses there work

	```
	cd ..
	python users_recently_active.py
	```
	
1. Write your own scripts	
	
