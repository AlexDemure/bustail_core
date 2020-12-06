from fastapi import APIRouter, status
from backend.common.utils import get_cities

router = APIRouter()


@router.get(
    "/cities/",
    responses={
        status.HTTP_200_OK: {
            "description": "Получение списка городов в системе.",
            "content": {
                "application/json": {
                    "example": ['Москва', 'Челябинск', '...']
                }
            },
        },
    }
)
def get_cities_list() -> list:
    """Получение списка городов."""
    return get_cities()
