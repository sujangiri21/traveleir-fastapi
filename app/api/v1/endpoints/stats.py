from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.services.package_analytics import (
    build_package_health_figure,
    get_package_health_analytics,
)

router = APIRouter()


@router.get("/json")
async def package_health_json(
    db: AsyncSession = Depends(deps.get_db),
) -> dict[str, Any]:
    return await get_package_health_analytics(db)


@router.get("/visual")
async def package_health_visual(
    db: AsyncSession = Depends(deps.get_db),
) -> StreamingResponse:
    analytics = await get_package_health_analytics(db)
    image_bytes = build_package_health_figure(analytics)
    return StreamingResponse(
        iter([image_bytes]),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=package-health.png"},
    )
