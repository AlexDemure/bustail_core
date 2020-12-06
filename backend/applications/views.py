from fastapi import HTTPException

from backend.applications import schemas
from backend.applications.crud import application as application_crud
from backend.common.serializer import string_to_datetime, datetime_to_string
from fastapi import HTTPException

from backend.applications import schemas
from backend.applications.crud import application as application_crud
from backend.common.serializer import string_to_datetime, datetime_to_string
from backend.common.enums import BaseSystemErrors


async def create_application(account: dict, application_in: schemas.ApplicationBase) -> schemas.ApplicationData:
    assert isinstance(application_in, schemas.ApplicationBase), BaseSystemErrors.schema_wrong_format.value

    application_data = application_in.dict()

    if application_data.get("to_go_when"):
        to_go_when = string_to_datetime(application_data.pop("to_go_when"))
    else:
        to_go_when = None

    try:
        application_in = schemas.ApplicationCreate(
            account_id=account['id'],
            to_go_when=to_go_when,
            **application_data
        )
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    application_id = await application_crud.create(application_in)
    application = await application_crud.get(application_id)

    return schemas.ApplicationData(
        to_go_when=datetime_to_string(application.pop('to_go_when')),
        created_at=datetime_to_string(application.pop('created_at')),
        **application
    )
