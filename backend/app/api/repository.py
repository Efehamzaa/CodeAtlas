from fastapi import APIRouter
from app.schemas.repository import RepositoryRequest

router=APIRouter(
    prefix="/repositories",
    tags=["Repository"]
)


@router.post("/")
def create_repository(request:RepositoryRequest):
    return {
    "status": "accepted",
    "message": "Repository accepted for analysis.",
    "url": request.url
}