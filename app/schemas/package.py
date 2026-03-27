from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import datetime

class PackageAttributeBase(BaseModel):
    difficulty_type_id: Optional[int] = None
    specialist_id: Optional[int] = None
    testimonial_id: Optional[int] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    price: Optional[Decimal] = None
    show_price: Optional[int] = 1
    accommodation: Optional[str] = None
    max_altitude: Optional[Any] = None
    trip_code: Optional[str] = None
    transportation: Optional[str] = None
    group_size_min: Optional[int] = None
    duration: Optional[int] = None
    departure: Optional[str] = None
    trip_starts: Optional[str] = None
    trip_ends: Optional[str] = None
    best_seasons: Optional[str] = None
    duration_unit: Optional[str] = None
    itinerary_title: Optional[str] = None

class PackageAttributeRead(PackageAttributeBase):
    id: int
    package_id: int

    model_config = ConfigDict(from_attributes=True)

class PackageBase(BaseModel):
    uuid: str
    trailgis_map_id: Optional[str] = None
    trailgis_summary_response: Optional[str] = None
    name: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
    is_complete: bool = False
    user_id: Optional[int] = None
    trip_agent_id: Optional[int] = None

class PackageRead(PackageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    attribute: Optional[PackageAttributeRead] = None

    model_config = ConfigDict(from_attributes=True)

class PackageList(BaseModel):
    items: List[PackageRead]
    total: int
    page: int
    size: int
    pages: int
