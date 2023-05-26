import importlib.metadata
import logging
import os

import uvicorn
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware

import db
from src import public, protected
from src.commons import settings

current_directory = os.path.dirname(os.path.realpath(__file__))

from fastapi import FastAPI, status, Depends, HTTPException

api_keys = [
    settings.DANS_LDN_INBOX_SERVICE_API_KEY
]  # Todo: This is encrypted in the .secrets.toml

# Authorization Form: It doesn't matter what you type in the form, it won't work yet. But we'll get there.
# See: https://fastapi.tiangolo.com/tutorial/security/first-steps/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


# settings = Dynaconf(
#     settings_files=[f"{current_directory}/conf/settings.toml", f"{current_directory}/conf/.secrets.toml"],
# )

__version__ = importlib.metadata.metadata("dans-ldn-inbox-service")["version"]

log = logging.getLogger(__name__)
app = FastAPI(title=settings.FASTAPI_TITLE, description=settings.FASTAPI_DESCRIPTION,
              version=__version__)

app.include_router(
    public.router,
    tags=["Public"],
    prefix=""
)

app.include_router(
    protected.router,
    tags=["Protected"],
    prefix="",
    dependencies=[Depends(api_key_auth)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    if settings.current_env == "DOCKER":  # this is the initial default
        print('name: ', settings.NAME)
    print('data_db_file', settings.data_db_file)
    print(settings.ROOT_PATH_FOR_DYNACONF)

    sql_create_inbox_table = """ CREATE TABLE `inbox` (`id` uuid,`created_time` datetime,`updated_time` datetime,
                                    `deleted_time` datetime,`sender` text,`payload` text, `payload_turtle` text,`valid_rdf` numeric,PRIMARY KEY (`id`));"""
    # todo: if not found, creates one.

    # create a database connection
    conn = db.create_sqlite3_connection(settings.data_db_file)

    # create tables
    if conn is not None:
        # create inbox table
        db.create_table(conn, sql_create_inbox_table)
    else:
        print("Error! cannot create the database connection.")

    uvicorn.run(app, host="0.0.0.0", port=1210)
    # uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)

# curl -D - -X POST -H "Content-Type: application/ld+json" -d @json-ld-example.json  http://localhost/inbox
# curl -i -X POST -d '<eko> <works> <DANS> .' -H'Content-Type: text/turtle'  http://127.0.0.1:1012/inbox
