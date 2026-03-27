from sqlalchemy import Column, Integer, String, Text, BigInteger, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

class PackageAttribute(Base):
    __tablename__ = 'package_attributes'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    package_id = Column(BigInteger, ForeignKey('packages.id'), unique=True, nullable=False)
    
    difficulty_type_id = Column(BigInteger, nullable=True)
    specialist_id = Column(BigInteger, nullable=True)
    testimonial_id = Column(BigInteger, nullable=True)
    country_id = Column(BigInteger, nullable=True)
    region_id = Column(BigInteger, nullable=True)
    
    price = Column(Numeric(precision=10, scale=2), nullable=True)
    show_price = Column(Integer, default=1)
    accommodation = Column(String(255), nullable=True)
    max_altitude = Column(String(255), nullable=True)
    trip_code = Column(String(255), nullable=True)
    transportation = Column(String(255), nullable=True)
    group_size_min = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    departure = Column(String(255), nullable=True)
    trip_starts = Column(String(255), nullable=True)
    trip_ends = Column(String(255), nullable=True)
    best_seasons = Column(String(255), nullable=True)
    
    duration_unit = Column(String(255), nullable=True)
    itinerary_title = Column(String(255), nullable=True)

    # Relationship back to Package
    package = relationship("Package", back_populates="attribute")
