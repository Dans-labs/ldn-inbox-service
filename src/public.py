from fastapi import APIRouter
from fastapi.openapi.models import Response
from starlette.responses import JSONResponse

import src
from src import db
from src.commons import settings

router = APIRouter()


@router.get('/inbox')
def get_inbox():
    content = db.select_all_inboxes(settings.data_db_file)
    # return JSONResponse(content={"eko":"test"}, headers=headers)
    return JSONResponse(status_code=200, content=content)


@router.get('/inbox/{recid}')
def get_inbox(recid: str):
    content = db.select_inbox_by_id(settings.data_db_file, recid)

    return JSONResponse(status_code=200, content=content)


# @router.get('/inbox/{target:path}/{updated_time}')
# def get_inbox(target: str, updated_time):
#     print(f'hello{target} and {updated_time}')
#     content = db.select_inbox_by_target_and_updated(settings.data_db_file, target, updated_time)
#
#     return JSONResponse(status_code=200, content=content)


@router.get('/inbox/updated_since/{updated_time}')#TODO: other endpoint name
def get_inbox(updated_time):
    print(f'{updated_time}')
    content = db.select_inbox_by_updated_time(settings.data_db_file, updated_time)

    return JSONResponse(status_code=200, content=content)

@router.head("/")
@router.get('/')
def about(response: Response):
    response.headers['X-Powered-By'] = 'https://github.com/ekoi/dans-inbox'
    # response.headers[
    #     'Link'] = '<' + 'http://localhost:1012/inbox' + '>; rel="http://www.w3.org/ns/ldp#inbox", <http://www.w3.org/ns/ldp#Resource>; rel="type", <http://www.w3.org/ns/ldp#RDFSource>; rel="type"'
    response.headers['Allow'] = "GET, HEAD, POST"
    response.headers[
        'Link'] = '<http://www.w3.org/ns/ldp#Resource>; rel="type", <http://www.w3.org/ns/ldp#RDFSource>; rel="type", <http://www.w3.org/ns/ldp#Container>; rel="type", <http://www.w3.org/ns/ldp#BasicContainer>; rel="type"'
    response.headers['Accept-Post'] = 'application/ld+json, text/turtle'
    return {"name": "LDN Inbox", "version": __version__}


@router.get('/version')
def version():
    return {"name": "DANS LDN Inbox Service", "version": src.commons.__version__}