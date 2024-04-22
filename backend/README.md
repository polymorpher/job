### Working directory

Unless otherwise specified, use `/backend` as your current working directory

See below for execution settings. You may also use .env for environment variables

### Initialize Python virtual environment

First, make sure [`virtualenv`](https://virtualenv.pypa.io/en/latest/) is installed. Then, use the setup script at the working directory: `/backend`

```
./setup.sh
```

### Install dependencies

```
pip install -r requirements.txt
```

### Initialize database schemas

```
python manage.py migrate 
```


### Development

```
export SSL_ENABLED=0
export USE_LOCAL_DB=1
python manage.py runserver
```


### Production

```
export SSL_ENABLED=1
export USE_LOCAL_DB=0
python manage.py runserver
```