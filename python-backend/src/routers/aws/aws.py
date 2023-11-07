from fastapi import APIRouter
from routers.aws import job, auth, repo, s3


router = APIRouter(prefix="/aws")
router.include_router(job.router)
router.include_router(auth.router)
router.include_router(repo.router)
router.include_router(s3.router)





