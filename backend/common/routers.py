from fastapi import APIRouter, status
from backend.common.utils import get_cities

router = APIRouter()


@router.get(
    "/cities/",
    responses={
        status.HTTP_200_OK: {
            "description": "Getting a list of cities in the system.",
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
