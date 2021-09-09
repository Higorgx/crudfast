	# Server-side FastAPI/Python app:
### This project uses MariaDB database
### Remember to set-up your database irl on alembic.init and /server/program/db/database.py

## Pre-Install
```sh
$ sudo apt-get install libpq-dev
$ sudo apt install libmariadb3 libmariadb-dev
```


## Install
```sh
$ pip3 install virtualenv
$ python3.8 -m venv env
```

## Run
```sh
$ source env/bin/activate
(env)$ pip3 install -r requirements.txt
(env)$ uvicorn app:app --reload
```

## Migrate


### Auto generate from models
```sh
(env)$ alembic revision --autogenerate -m "put a nice message here"
```

### Run all migrations
```sh
(env)$ alembic upgrade head
```

