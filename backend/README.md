Working directory: `/backend`

See below for execution settings. You may also use .env for environment variables

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