# new

```shell
python3 -m venv env      

source env/bin/activate
```

```shell
poetry install
```

```shell
cd /src/.env

SECRET_KEY=<random string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

```shell 

cd /src

uvicorn main:app --host 0.0.0.0 --port 80

```

```logs
(env) ➜  src git:(main) uvicorn main:app --host 0.0.0.0 --port 80
INFO:     Started server process [97555]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```