import json
import uuid
from datetime import datetime

# import codecs
from fastapi import APIRouter, Request, status, UploadFile
from rdflib import Graph
from starlette.responses import JSONResponse

from src import db
from src.commons import settings, ACCEPTED_CONTENT_TYPES, headers

router = APIRouter()


@router.get("/settings")
async def get_settings():
    return settings

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print("eko")
    return {"filename": file.filename}
@router.head("/inbox")
@router.post('/inbox')
async def post_inbox(submitted_json_ld: Request):
    s_json_ld_obj = await submitted_json_ld.json()
    graph = Graph()
    content_type = submitted_json_ld.headers['Content-Type']
    if content_type in ACCEPTED_CONTENT_TYPES:
        print(content_type)
        graph.parse(data=s_json_ld_obj, format=content_type)
        text_turtle = graph.serialize(format='text/turtle')
        # create a database connection
        conn = db.create_sqlite3_connection(settings.data_db_file)
        with conn:
            # create a new record
            record = (
                str(uuid.uuid4()), datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f"), datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f"), submitted_json_ld.client.host, json.dumps(s_json_ld_obj),
                text_turtle);
            record_id = db.create_inbox_record(conn, record)
            print(f'LDN INBOX: {record_id}')
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=str(record_id), headers=headers(str(record_id)))
    else:
        return 401

    return 201
