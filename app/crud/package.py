from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.models.package import Package
from app.models.package_attribute import PackageAttribute

async def get_packages(db: AsyncSession, page: int = 1, size: int = 10):
    offset = (page - 1) * size
    
    # Query for items with joined attribute
    query = (
        select(Package)
        .options(joinedload(Package.attribute))
        .offset(offset)
        .limit(size)
    )
    result = await db.execute(query)
    items = result.unique().scalars().all()
    
    # Query for total count
    count_query = select(func.count(Package.id))
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return items, total

async def get_package(db: AsyncSession, package_id: int):
    query = (
        select(Package)
        .options(joinedload(Package.attribute))
        .filter(Package.id == package_id)
    )
    result = await db.execute(query)
    return result.unique().scalar_one_or_none()
