from fastapi import APIRouter
from routers.aws import job, auth, repo


router = APIRouter(prefix="/aws")
router.include_router(job.router)
router.include_router(auth.router)
router.include_router(repo.router)





