from sqlalchemy import Column, Integer, String, Boolean, Text, BigInteger, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Package(Base):
    __tablename__ = 'packages'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String(36), unique=True, index=True)
    trailgis_map_id = Column(String(255), nullable=True)
    trailgis_summary_response = Column(Text, nullable=True)
    name = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_complete = Column(Boolean, default=False)
    user_id = Column(BigInteger, nullable=True)
    trip_agent_id = Column(BigInteger, nullable=True)
    
    # Laravel timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship 1:1 with PackageAttribute
    attribute = relationship("PackageAttribute", back_populates="package", uselist=False)
