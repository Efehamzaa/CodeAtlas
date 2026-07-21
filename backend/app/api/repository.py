from fastapi import APIRouter

router=APIRouter(
    prefix="/repositories",
    tags=["Repository"]
)


@router.post("/")
def create_repository():
    return {
    "status": "accepted",
    "message": "Repository accepted for analysis."
}