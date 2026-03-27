from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.crud import package as crud_package
from app.schemas.package import PackageRead, PackageList

router = APIRouter()

@router.get("/", response_model=PackageList)
async def read_packages(
    db: AsyncSession = Depends(deps.get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
) -> Any:
    """
    Retrieve packages with pagination and attribute information.
    """
    items, total = await crud_package.get_packages(db, page=page, size=size)
    pages = (total + size - 1) // size
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

@router.get("/{id}", response_model=PackageRead)
async def read_package(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get a single package by its primary key ID.
    """
    package = await crud_package.get_package(db, package_id=id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package
