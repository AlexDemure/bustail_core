from fastapi import APIRouter, HTTPException, Depends

from accounts import schemas, logic, service, models, serializer
from authorization.utils import get_current_user
from common.schemas import UpdateBase

router = APIRouter()


@router.post("/", response_model=schemas.Account)
async def create_account(request: schemas.AccountCreate):
    """Создание пользовательского аккаунта."""
    personal_data = await service.PersonalDataService.get_by_attribute('phone', request.personal_data.phone)
    if personal_data:
        raise HTTPException(status_code=400, detail="Phone number associated with another account.")

    auth_data = await service.AuthorizationDataService.get_by_login(request.authorization_data.login)
    if auth_data:
        raise HTTPException(status_code=400, detail="Login associated with another account.")

    return await logic.create_account(request)


@router.get("/", response_model=schemas.Account)
async def get_account(account: models.Account = Depends(get_current_user)):
    """Получение аккаунта только при наличии токена авторизации."""
    return serializer.AccountSerializer.prepared_data(**dict(account))


@router.put('/personal_data', response_model=schemas.Account)
async def update_person_data(request: schemas.PersonalDataBase, account: models.Account = Depends(get_current_user)):
    """Обновление персональных данных только при наличии токена авторизации."""
    personal_data = await service.PersonalDataService.get_by_attribute('phone', request.phone, account.id)
    if personal_data:
        raise HTTPException(status_code=400, detail="Phone number associated with another account.")

    personal_data = await service.PersonalDataService.get_by_account_id(account.id)
    if not personal_data:
        raise HTTPException(status_code=400, detail="Personal data is not found")

    schema = UpdateBase(id=account.id, updated_fields=request.dict())
    await logic.update_personal_data(schema)

