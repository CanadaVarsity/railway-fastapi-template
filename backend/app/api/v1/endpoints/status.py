import os
import time
from fastapi import APIRouter

BUILD_STAMP = (
    os.getenv("RAILWAY_DEPLOYMENT_ID")
    or os.getenv("RAILWAY_GIT_COMMIT_SHA")
    or f"manual-{int(time.time())}"
)

router = APIRouter()

@router.get("/status")
async def v1_status():
    return {
        "status": "operational_DEPLOY_PROOF_1767757600",
        "build": BUILD_STAMP,
        "marker": "TRUTH_BASELINE",
    }
