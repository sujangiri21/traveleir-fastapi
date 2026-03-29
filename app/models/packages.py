from typing import Optional
import datetime
import decimal
import enum

from sqlalchemy import CHAR, Computed, DECIMAL, Date, Double, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class ImagesFileType(str, enum.Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    PDF = 'pdf'
    DOC = 'doc'
    OTHER = 'other'


class ImagesProcessingStatus(str, enum.Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class ImagesStorageDriver(str, enum.Enum):
    LOCAL = 'local'
    S3 = 's3'


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='roles_user_id_foreign'),
        Index('roles_role_unique', 'role', unique=True),
        Index('roles_user_id_foreign', 'user_id'),
        Index('roles_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    is_super: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    user_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[user_id], back_populates='roles_user')
    users_role: Mapped[list['Users']] = relationship('Users', foreign_keys='[Users.role_id]', back_populates='role')


class Testimonials(Base):
    __tablename__ = 'testimonials'
    __table_args__ = (
        Index('testimonials_name_unique', 'name', unique=True),
        Index('testimonials_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    stars: Mapped[decimal.Decimal] = mapped_column(Double(asdecimal=True), nullable=False, server_default=text('1'))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    position: Mapped[Optional[str]] = mapped_column(String(255))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    source: Mapped[Optional[str]] = mapped_column(String(255))
    published_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    image_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    display_order: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    user_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    image_title: Mapped[Optional[str]] = mapped_column(String(255))
    image_caption: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    package_testimonials: Mapped[list['PackageTestimonials']] = relationship('PackageTestimonials', back_populates='testimonial')
    package_attributes: Mapped[list['PackageAttributes']] = relationship('PackageAttributes', back_populates='testimonial')


class TripAgents(Base):
    __tablename__ = 'trip_agents'

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    add_to_home: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('0'))
    short_description: Mapped[Optional[str]] = mapped_column(Text)
    long_description: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    keywords: Mapped[Optional[str]] = mapped_column(Text)
    logo: Mapped[Optional[str]] = mapped_column(String(255))
    inverse_logo: Mapped[Optional[str]] = mapped_column(String(255))
    contact_number: Mapped[Optional[str]] = mapped_column(String(255))
    website_link: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    mobile: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    users: Mapped[list['Users']] = relationship('Users', back_populates='trip_agent')
    images: Mapped[list['Images']] = relationship('Images', back_populates='trip_agent')
    packages: Mapped[list['Packages']] = relationship('Packages', back_populates='trip_agent')


class UserTypes(Base):
    __tablename__ = 'user_types'

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    users: Mapped[list['Users']] = relationship('Users', back_populates='user_type')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='users_role_id_foreign'),
        ForeignKeyConstraint(['trip_agent_id'], ['trip_agents.id'], name='user_trip_agent_fk'),
        ForeignKeyConstraint(['user_type_id'], ['user_types.id'], ondelete='CASCADE', name='user_type_foreign'),
        Index('user_trip_agent_fk', 'trip_agent_id'),
        Index('user_type_foreign', 'user_type_id'),
        Index('users_email_unique', 'email', unique=True),
        Index('users_role_id_foreign', 'role_id'),
        Index('users_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    force_reset_password: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('0'))
    user_type_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    trip_agent_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    email_verified_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    two_factor_secret: Mapped[Optional[str]] = mapped_column(Text)
    two_factor_recovery_codes: Mapped[Optional[str]] = mapped_column(Text)
    remember_token: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    roles_user: Mapped[list['Roles']] = relationship('Roles', foreign_keys='[Roles.user_id]', back_populates='user')
    role: Mapped['Roles'] = relationship('Roles', foreign_keys=[role_id], back_populates='users_role')
    trip_agent: Mapped[Optional['TripAgents']] = relationship('TripAgents', back_populates='users')
    user_type: Mapped[Optional['UserTypes']] = relationship('UserTypes', back_populates='users')
    images: Mapped[list['Images']] = relationship('Images', back_populates='user')
    meal_plans: Mapped[list['MealPlans']] = relationship('MealPlans', back_populates='user')
    pages: Mapped[list['Pages']] = relationship('Pages', back_populates='user')
    trip_addons: Mapped[list['TripAddons']] = relationship('TripAddons', back_populates='user')
    activities: Mapped[list['Activities']] = relationship('Activities', back_populates='user')
    countries: Mapped[list['Countries']] = relationship('Countries', back_populates='user')
    destinations: Mapped[list['Destinations']] = relationship('Destinations', back_populates='user')
    difficulty_types: Mapped[list['DifficultyTypes']] = relationship('DifficultyTypes', back_populates='user')
    hotels: Mapped[list['Hotels']] = relationship('Hotels', back_populates='user')
    specialists: Mapped[list['Specialists']] = relationship('Specialists', back_populates='user')
    regions: Mapped[list['Regions']] = relationship('Regions', back_populates='user')


class Images(Base):
    __tablename__ = 'images'
    __table_args__ = (
        ForeignKeyConstraint(['trip_agent_id'], ['trip_agents.id'], name='image_trip_agent_fk'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='images_user_id_foreign'),
        Index('image_trip_agent_fk', 'trip_agent_id'),
        Index('images_user_id_foreign', 'user_id'),
        Index('images_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    file_type: Mapped[ImagesFileType] = mapped_column(Enum(ImagesFileType, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('1'))
    processing_status: Mapped[ImagesProcessingStatus] = mapped_column(Enum(ImagesProcessingStatus, values_callable=lambda cls: [member.value for member in cls]), nullable=False, server_default=text("'pending'"))
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text)
    caption: Mapped[Optional[str]] = mapped_column(Text)
    size_in_kb: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    resolution: Mapped[Optional[str]] = mapped_column(String(50))
    aspect_ratio: Mapped[Optional[str]] = mapped_column(String(50))
    storage_driver: Mapped[Optional[ImagesStorageDriver]] = mapped_column(Enum(ImagesStorageDriver, values_callable=lambda cls: [member.value for member in cls]))
    hls_master_playlist_path: Mapped[Optional[str]] = mapped_column(String(512))
    hls_segment_paths: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    thumbnail_path: Mapped[Optional[str]] = mapped_column(String(512))
    processing_log: Mapped[Optional[str]] = mapped_column(Text)
    duration_in_seconds: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    trip_agent_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    trip_agent: Mapped[Optional['TripAgents']] = relationship('TripAgents', back_populates='images')
    user: Mapped['Users'] = relationship('Users', back_populates='images')
    activities: Mapped[list['Activities']] = relationship('Activities', back_populates='image')
    countries: Mapped[list['Countries']] = relationship('Countries', back_populates='image')
    destinations: Mapped[list['Destinations']] = relationship('Destinations', back_populates='image')
    difficulty_types: Mapped[list['DifficultyTypes']] = relationship('DifficultyTypes', back_populates='image')
    hotels: Mapped[list['Hotels']] = relationship('Hotels', back_populates='image')
    package_images: Mapped[list['PackageImages']] = relationship('PackageImages', back_populates='image')
    package_map_images: Mapped[list['PackageMapImages']] = relationship('PackageMapImages', back_populates='image')
    package_maps: Mapped[list['PackageMaps']] = relationship('PackageMaps', back_populates='image')
    package_seos: Mapped[list['PackageSeos']] = relationship('PackageSeos', back_populates='image')
    package_videos: Mapped[list['PackageVideos']] = relationship('PackageVideos', back_populates='image')
    specialists: Mapped[list['Specialists']] = relationship('Specialists', back_populates='image')
    regions: Mapped[list['Regions']] = relationship('Regions', back_populates='image')
    package_itinerary_images: Mapped[list['PackageItineraryImages']] = relationship('PackageItineraryImages', back_populates='image')


class MealPlans(Base):
    __tablename__ = 'meal_plans'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='meal_plans_user_id_foreign'),
        Index('meal_plans_name_unique', 'name', unique=True),
        Index('meal_plans_user_id_foreign', 'user_id'),
        Index('meal_plans_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='meal_plans')
    package_itineraries: Mapped[list['PackageItineraries']] = relationship('PackageItineraries', back_populates='meal_plan')


class Packages(Base):
    __tablename__ = 'packages'
    __table_args__ = (
        ForeignKeyConstraint(['trip_agent_id'], ['trip_agents.id'], name='package_trip_agent_fk'),
        Index('package_trip_agent_fk', 'trip_agent_id'),
        Index('packages_name_unique', 'name', unique=True),
        Index('packages_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    trailgis_map_id: Mapped[Optional[str]] = mapped_column(String(255))
    trailgis_summary_response: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    subtitle: Mapped[Optional[str]] = mapped_column(Text)
    is_complete: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    add_to_home: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    is_signature: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    is_culture_tour: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    user_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    trip_agent_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    trip_agent: Mapped[Optional['TripAgents']] = relationship('TripAgents', back_populates='packages')
    package_accommodations: Mapped[list['PackageAccommodations']] = relationship('PackageAccommodations', back_populates='package')
    package_destination: Mapped[list['PackageDestination']] = relationship('PackageDestination', back_populates='package')
    package_essential_informations: Mapped[list['PackageEssentialInformations']] = relationship('PackageEssentialInformations', back_populates='package')
    package_extensions: Mapped[list['PackageExtensions']] = relationship('PackageExtensions', back_populates='package')
    package_extras: Mapped[list['PackageExtras']] = relationship('PackageExtras', back_populates='package')
    package_faqs: Mapped[list['PackageFaqs']] = relationship('PackageFaqs', back_populates='package')
    package_fix_departures: Mapped[list['PackageFixDepartures']] = relationship('PackageFixDepartures', back_populates='package')
    package_highlights: Mapped[list['PackageHighlights']] = relationship('PackageHighlights', back_populates='package')
    package_images: Mapped[list['PackageImages']] = relationship('PackageImages', back_populates='package')
    package_important_informations: Mapped[list['PackageImportantInformations']] = relationship('PackageImportantInformations', back_populates='package')
    package_includes_excludes: Mapped[list['PackageIncludesExcludes']] = relationship('PackageIncludesExcludes', back_populates='package')
    package_map_images: Mapped[list['PackageMapImages']] = relationship('PackageMapImages', back_populates='package')
    package_maps: Mapped[list['PackageMaps']] = relationship('PackageMaps', back_populates='package')
    package_overviews: Mapped[list['PackageOverviews']] = relationship('PackageOverviews', back_populates='package')
    package_policies: Mapped[list['PackagePolicies']] = relationship('PackagePolicies', back_populates='package')
    package_seos: Mapped[list['PackageSeos']] = relationship('PackageSeos', back_populates='package')
    package_testimonials: Mapped[list['PackageTestimonials']] = relationship('PackageTestimonials', back_populates='package')
    package_trip_addons: Mapped[list['PackageTripAddons']] = relationship('PackageTripAddons', back_populates='package')
    package_videos: Mapped[list['PackageVideos']] = relationship('PackageVideos', back_populates='package')
    package_activities: Mapped[list['PackageActivities']] = relationship('PackageActivities', back_populates='package')
    package_bookings: Mapped[list['PackageBookings']] = relationship('PackageBookings', back_populates='package')
    package_itineraries: Mapped[list['PackageItineraries']] = relationship('PackageItineraries', back_populates='package')
    package_specialists: Mapped[list['PackageSpecialists']] = relationship('PackageSpecialists', back_populates='package')
    package_attributes: Mapped[list['PackageAttributes']] = relationship('PackageAttributes', back_populates='package')


class Pages(Base):
    __tablename__ = 'pages'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='pages_user_id_foreign'),
        Index('pages_name_unique', 'name', unique=True),
        Index('pages_user_id_foreign', 'user_id'),
        Index('pages_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    header_id: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    footer_id: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    is_home: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='pages')
    activities: Mapped[list['Activities']] = relationship('Activities', back_populates='page')
    countries: Mapped[list['Countries']] = relationship('Countries', back_populates='page')
    destinations: Mapped[list['Destinations']] = relationship('Destinations', back_populates='page')
    hotels: Mapped[list['Hotels']] = relationship('Hotels', back_populates='page')
    regions: Mapped[list['Regions']] = relationship('Regions', back_populates='page')


class TripAddons(Base):
    __tablename__ = 'trip_addons'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='trip_addons_user_id_foreign'),
        Index('trip_addons_name_unique', 'name', unique=True),
        Index('trip_addons_user_id_foreign', 'user_id'),
        Index('trip_addons_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='trip_addons')
    package_trip_addons: Mapped[list['PackageTripAddons']] = relationship('PackageTripAddons', back_populates='trip_addon')


class Activities(Base):
    __tablename__ = 'activities'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='activities_image_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='SET NULL', name='activities_page_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='activities_user_id_foreign'),
        Index('activities_image_id_foreign', 'image_id'),
        Index('activities_name_unique', 'name', unique=True),
        Index('activities_page_id_foreign', 'page_id'),
        Index('activities_user_id_foreign', 'user_id'),
        Index('activities_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    add_to_home: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('0'))
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    page_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='activities')
    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='activities')
    user: Mapped['Users'] = relationship('Users', back_populates='activities')
    package_activities: Mapped[list['PackageActivities']] = relationship('PackageActivities', back_populates='activity')


class Countries(Base):
    __tablename__ = 'countries'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='countries_image_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='SET NULL', name='countries_page_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='countries_user_id_foreign'),
        Index('countries_code_unique', 'code', unique=True),
        Index('countries_image_id_foreign', 'image_id'),
        Index('countries_name_unique', 'name', unique=True),
        Index('countries_page_id_foreign', 'page_id'),
        Index('countries_user_id_foreign', 'user_id'),
        Index('countries_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    phone_code: Mapped[Optional[str]] = mapped_column(String(32))
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    page_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    user_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='countries')
    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='countries')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='countries')
    regions: Mapped[list['Regions']] = relationship('Regions', back_populates='country')
    package_attributes: Mapped[list['PackageAttributes']] = relationship('PackageAttributes', back_populates='country')
    package_booking_travellers: Mapped[list['PackageBookingTravellers']] = relationship('PackageBookingTravellers', back_populates='country')


class Destinations(Base):
    __tablename__ = 'destinations'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='destinations_image_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='SET NULL', name='destinations_page_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='destinations_user_id_foreign'),
        Index('destinations_image_id_foreign', 'image_id'),
        Index('destinations_name_unique', 'name', unique=True),
        Index('destinations_page_id_foreign', 'page_id'),
        Index('destinations_user_id_foreign', 'user_id'),
        Index('destinations_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    page_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='destinations')
    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='destinations')
    user: Mapped['Users'] = relationship('Users', back_populates='destinations')
    package_attributes: Mapped[list['PackageAttributes']] = relationship('PackageAttributes', back_populates='destination')


class DifficultyTypes(Base):
    __tablename__ = 'difficulty_types'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='difficulty_types_image_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='difficulty_types_user_id_foreign'),
        Index('difficulty_types_image_id_foreign', 'image_id'),
        Index('difficulty_types_name_unique', 'name', unique=True),
        Index('difficulty_types_user_id_foreign', 'user_id'),
        Index('difficulty_types_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='difficulty_types')
    user: Mapped['Users'] = relationship('Users', back_populates='difficulty_types')
    package_attributes: Mapped[list['PackageAttributes']] = relationship('PackageAttributes', back_populates='difficulty_type')


class Hotels(Base):
    __tablename__ = 'hotels'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='hotels_image_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='SET NULL', name='hotels_page_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='hotels_user_id_foreign'),
        Index('hotels_image_id_foreign', 'image_id'),
        Index('hotels_name_unique', 'name', unique=True),
        Index('hotels_page_id_foreign', 'page_id'),
        Index('hotels_user_id_foreign', 'user_id'),
        Index('hotels_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    address: Mapped[Optional[str]] = mapped_column(Text)
    emails: Mapped[Optional[str]] = mapped_column(Text)
    phones: Mapped[Optional[str]] = mapped_column(Text)
    page_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='hotels')
    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='hotels')
    user: Mapped['Users'] = relationship('Users', back_populates='hotels')
    package_itineraries: Mapped[list['PackageItineraries']] = relationship('PackageItineraries', back_populates='hotel')


class PackageAccommodations(Base):
    __tablename__ = 'package_accommodations'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_accommodations_package_id_foreign'),
        Index('package_accommodations_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_accommodations')


class PackageDestination(Base):
    __tablename__ = 'package_destination'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], name='package_destination_package_id_foreign'),
        Index('package_destination_package_id_destination_id_unique', 'package_id', 'destination_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    destination_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_destination')


class PackageEssentialInformations(Base):
    __tablename__ = 'package_essential_informations'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_essential_informations_package_id_foreign'),
        Index('package_essential_informations_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    subtitle: Mapped[Optional[str]] = mapped_column(Text)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_essential_informations')


class PackageExtensions(Base):
    __tablename__ = 'package_extensions'
    __table_args__ = (
        ForeignKeyConstraint(['package_extension_id'], ['package_extensions.id'], ondelete='CASCADE', name='package_extensions_package_extension_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_extensions_package_id_foreign'),
        Index('package_extensions_package_extension_id_foreign', 'package_extension_id'),
        Index('package_extensions_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    package_extension_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    package_extension: Mapped['PackageExtensions'] = relationship('PackageExtensions', remote_side=[id], back_populates='package_extension_reverse')
    package_extension_reverse: Mapped[list['PackageExtensions']] = relationship('PackageExtensions', remote_side=[package_extension_id], back_populates='package_extension')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_extensions')


class PackageExtras(Base):
    __tablename__ = 'package_extras'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_extras_package_id_foreign'),
        Index('package_extras_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    equipment_check_list: Mapped[Optional[str]] = mapped_column(Text)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_extras')


class PackageFaqs(Base):
    __tablename__ = 'package_faqs'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_faqs_package_id_foreign'),
        Index('package_faqs_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    display_order: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_faqs')


class PackageFixDepartures(Base):
    __tablename__ = 'package_fix_departures'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_fix_departures_package_id_foreign'),
        Index('package_fix_departures_package_id_foreign', 'package_id'),
        Index('package_fix_departures_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    departing_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    finishing_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    actual_price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(13, 2), nullable=False)
    discounted_price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(13, 2), nullable=False)
    pricing_description: Mapped[Optional[str]] = mapped_column(Text)
    availability_text: Mapped[Optional[str]] = mapped_column(String(255))

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_fix_departures')
    package_bookings: Mapped[list['PackageBookings']] = relationship('PackageBookings', back_populates='fix_departure')


class PackageHighlights(Base):
    __tablename__ = 'package_highlights'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_highlights_package_id_foreign'),
        Index('package_highlights_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_highlights')


class PackageImages(Base):
    __tablename__ = 'package_images'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='package_images_image_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_images_package_id_foreign'),
        Index('package_images_image_id_foreign', 'image_id'),
        Index('package_images_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    display_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    image: Mapped['Images'] = relationship('Images', back_populates='package_images')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_images')


class PackageImportantInformations(Base):
    __tablename__ = 'package_important_informations'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_important_informations_package_id_foreign'),
        Index('package_important_informations_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_important_informations')


class PackageIncludesExcludes(Base):
    __tablename__ = 'package_includes_excludes'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_includes_excludes_package_id_foreign'),
        Index('package_includes_excludes_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    includes: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    excludes: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    includes_title: Mapped[Optional[str]] = mapped_column(String(255))
    excludes_title: Mapped[Optional[str]] = mapped_column(String(255))

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_includes_excludes')


class PackageMapImages(Base):
    __tablename__ = 'package_map_images'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='package_map_images_image_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_map_images_package_id_foreign'),
        Index('package_map_images_image_id_foreign', 'image_id'),
        Index('package_map_images_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    display_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    image: Mapped['Images'] = relationship('Images', back_populates='package_map_images')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_map_images')


class PackageMaps(Base):
    __tablename__ = 'package_maps'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='package_maps_image_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_maps_package_id_foreign'),
        Index('package_maps_image_id_foreign', 'image_id'),
        Index('package_maps_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    display_order: Mapped[Optional[int]] = mapped_column(TINYINT(4))
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='package_maps')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_maps')


class PackageOverviews(Base):
    __tablename__ = 'package_overviews'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_overviews_package_id_foreign'),
        Index('package_overviews_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(LONGTEXT, nullable=False)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_overviews')


class PackagePolicies(Base):
    __tablename__ = 'package_policies'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_policies_package_id_foreign'),
        Index('package_policies_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_policies')


class PackageSeos(Base):
    __tablename__ = 'package_seos'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='package_seos_image_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_seos_package_id_foreign'),
        Index('package_seos_image_id_foreign', 'image_id'),
        Index('package_seos_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    meta_title: Mapped[str] = mapped_column(Text, nullable=False)
    meta_description: Mapped[str] = mapped_column(Text, nullable=False)
    meta_keywords: Mapped[str] = mapped_column(Text, nullable=False)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    image_alt: Mapped[Optional[str]] = mapped_column(Text)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='package_seos')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_seos')


class PackageTestimonials(Base):
    __tablename__ = 'package_testimonials'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_testimonials_package_id_foreign'),
        ForeignKeyConstraint(['testimonial_id'], ['testimonials.id'], ondelete='CASCADE', name='package_testimonials_testimonial_id_foreign'),
        Index('package_testimonials_package_id_foreign', 'package_id'),
        Index('package_testimonials_testimonial_id_foreign', 'testimonial_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    testimonial_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_testimonials')
    testimonial: Mapped['Testimonials'] = relationship('Testimonials', back_populates='package_testimonials')


class PackageTripAddons(Base):
    __tablename__ = 'package_trip_addons'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_trip_addons_package_id_foreign'),
        ForeignKeyConstraint(['trip_addon_id'], ['trip_addons.id'], ondelete='CASCADE', name='package_trip_addons_trip_addon_id_foreign'),
        Index('package_trip_addons_package_id_foreign', 'package_id'),
        Index('package_trip_addons_trip_addon_id_foreign', 'trip_addon_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    trip_addon_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_trip_addons')
    trip_addon: Mapped['TripAddons'] = relationship('TripAddons', back_populates='package_trip_addons')


class PackageVideos(Base):
    __tablename__ = 'package_videos'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='package_videos_image_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_videos_package_id_foreign'),
        Index('package_videos_image_id_foreign', 'image_id'),
        Index('package_videos_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='package_videos')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_videos')


class Specialists(Base):
    __tablename__ = 'specialists'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='specialists_image_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='specialists_user_id_foreign'),
        Index('specialists_image_id_foreign', 'image_id'),
        Index('specialists_name_unique', 'name', unique=True),
        Index('specialists_user_id_foreign', 'user_id'),
        Index('specialists_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    contact_number: Mapped[Optional[str]] = mapped_column(String(255))
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='specialists')
    user: Mapped['Users'] = relationship('Users', back_populates='specialists')
    package_specialists: Mapped[list['PackageSpecialists']] = relationship('PackageSpecialists', back_populates='specialist')
    package_attributes: Mapped[list['PackageAttributes']] = relationship('PackageAttributes', back_populates='specialist')


class PackageActivities(Base):
    __tablename__ = 'package_activities'
    __table_args__ = (
        ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='CASCADE', name='package_activities_activity_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_activities_package_id_foreign'),
        Index('package_activities_activity_id_foreign', 'activity_id'),
        Index('package_activities_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    activity_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)

    activity: Mapped['Activities'] = relationship('Activities', back_populates='package_activities')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_activities')


class PackageBookings(Base):
    __tablename__ = 'package_bookings'
    __table_args__ = (
        ForeignKeyConstraint(['fix_departure_id'], ['package_fix_departures.id'], ondelete='SET NULL', name='package_bookings_fix_departure_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_bookings_package_id_foreign'),
        Index('package_bookings_booking_code_unique', 'booking_code', unique=True),
        Index('package_bookings_fix_departure_id_foreign', 'fix_departure_id'),
        Index('package_bookings_package_id_foreign', 'package_id'),
        Index('package_bookings_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    booking_code: Mapped[str] = mapped_column(String(255), nullable=False)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    traveller_pax: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    terms_aggrement: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    expected_travel_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    fix_departure_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    departing_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    finishing_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    insurance: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    special_requirement: Mapped[Optional[str]] = mapped_column(Text)
    find_us_via: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    preferred_platform: Mapped[Optional[str]] = mapped_column(String(255), comment='Eg. whatsapp, wechat')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    fix_departure: Mapped[Optional['PackageFixDepartures']] = relationship('PackageFixDepartures', back_populates='package_bookings')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_bookings')
    package_booking_flight_details: Mapped[list['PackageBookingFlightDetails']] = relationship('PackageBookingFlightDetails', back_populates='package_booking')
    package_booking_travellers: Mapped[list['PackageBookingTravellers']] = relationship('PackageBookingTravellers', back_populates='package_booking')


class PackageItineraries(Base):
    __tablename__ = 'package_itineraries'
    __table_args__ = (
        ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ondelete='SET NULL', name='package_itineraries_hotel_id_foreign'),
        ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ondelete='SET NULL', name='package_itineraries_meal_plan_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_itineraries_package_id_foreign'),
        Index('package_itineraries_hotel_id_foreign', 'hotel_id'),
        Index('package_itineraries_meal_plan_id_foreign', 'meal_plan_id'),
        Index('package_itineraries_package_id_foreign', 'package_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    day: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    day_title: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    subtitle: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[Optional[str]] = mapped_column(String(32))
    longitude: Mapped[Optional[str]] = mapped_column(String(32))
    distance: Mapped[Optional[str]] = mapped_column(String(100))
    duration: Mapped[Optional[str]] = mapped_column(String(100))
    meal_plan_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    hotel_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    accommodation: Mapped[Optional[str]] = mapped_column(Text)
    other_details: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))

    hotel: Mapped[Optional['Hotels']] = relationship('Hotels', back_populates='package_itineraries')
    meal_plan: Mapped[Optional['MealPlans']] = relationship('MealPlans', back_populates='package_itineraries')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_itineraries')
    package_itinerary_images: Mapped[list['PackageItineraryImages']] = relationship('PackageItineraryImages', back_populates='package_itinerary')


class PackageSpecialists(Base):
    __tablename__ = 'package_specialists'
    __table_args__ = (
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_specialists_package_id_foreign'),
        ForeignKeyConstraint(['specialist_id'], ['specialists.id'], ondelete='CASCADE', name='package_specialists_specialist_id_foreign'),
        Index('package_specialists_package_id_foreign', 'package_id'),
        Index('package_specialists_specialist_id_foreign', 'specialist_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    specialist_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)

    package: Mapped['Packages'] = relationship('Packages', back_populates='package_specialists')
    specialist: Mapped['Specialists'] = relationship('Specialists', back_populates='package_specialists')


class Regions(Base):
    __tablename__ = 'regions'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='SET NULL', name='regions_country_id_foreign'),
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='regions_image_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='SET NULL', name='regions_page_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='regions_user_id_foreign'),
        Index('regions_code_unique', 'code', unique=True),
        Index('regions_country_id_foreign', 'country_id'),
        Index('regions_image_id_foreign', 'image_id'),
        Index('regions_name_unique', 'name', unique=True),
        Index('regions_page_id_foreign', 'page_id'),
        Index('regions_user_id_foreign', 'user_id'),
        Index('regions_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    country_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    page_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    country: Mapped[Optional['Countries']] = relationship('Countries', back_populates='regions')
    image: Mapped[Optional['Images']] = relationship('Images', back_populates='regions')
    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='regions')
    user: Mapped['Users'] = relationship('Users', back_populates='regions')
    package_attributes: Mapped[list['PackageAttributes']] = relationship('PackageAttributes', back_populates='region')


class PackageAttributes(Base):
    __tablename__ = 'package_attributes'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='SET NULL', name='package_attributes_country_id_foreign'),
        ForeignKeyConstraint(['destination_id'], ['destinations.id'], ondelete='SET NULL', name='package_attributes_destination_id_foreign'),
        ForeignKeyConstraint(['difficulty_type_id'], ['difficulty_types.id'], ondelete='SET NULL', name='package_attributes_difficulty_type_id_foreign'),
        ForeignKeyConstraint(['package_id'], ['packages.id'], ondelete='CASCADE', name='package_attributes_package_id_foreign'),
        ForeignKeyConstraint(['region_id'], ['regions.id'], ondelete='SET NULL', name='package_attributes_region_id_foreign'),
        ForeignKeyConstraint(['specialist_id'], ['specialists.id'], ondelete='SET NULL', name='package_attributes_specialist_id_foreign'),
        ForeignKeyConstraint(['testimonial_id'], ['testimonials.id'], ondelete='SET NULL', name='package_attributes_testimonial_id_foreign'),
        Index('package_attributes_country_id_foreign', 'country_id'),
        Index('package_attributes_destination_id_foreign', 'destination_id'),
        Index('package_attributes_difficulty_type_id_foreign', 'difficulty_type_id'),
        Index('package_attributes_package_id_foreign', 'package_id'),
        Index('package_attributes_region_id_foreign', 'region_id'),
        Index('package_attributes_specialist_id_foreign', 'specialist_id'),
        Index('package_attributes_testimonial_id_foreign', 'testimonial_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    duration: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    destination_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    region_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    country_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    specialist_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    testimonial_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    duration_unit: Mapped[Optional[str]] = mapped_column(String(255))
    itinerary_title: Mapped[Optional[str]] = mapped_column(String(255))
    departure: Mapped[Optional[str]] = mapped_column(String(255))
    best_seasons: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    group_size_min: Mapped[Optional[str]] = mapped_column(String(255))
    transportation: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[Optional[str]] = mapped_column(String(255))
    show_price: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    max_altitude: Mapped[Optional[int]] = mapped_column(INTEGER(10, unsigned=True))
    altitude_range: Mapped[Optional[int]] = mapped_column(INTEGER(10, unsigned=True), Computed('(floor(`max_altitude` / 1000) * 1000)', persisted=True))
    difficulty_type_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    trip_starts: Mapped[Optional[str]] = mapped_column(String(255))
    trip_ends: Mapped[Optional[str]] = mapped_column(String(255))
    trip_code: Mapped[Optional[str]] = mapped_column(String(255))
    accommodation: Mapped[Optional[str]] = mapped_column(Text)

    country: Mapped[Optional['Countries']] = relationship('Countries', back_populates='package_attributes')
    destination: Mapped[Optional['Destinations']] = relationship('Destinations', back_populates='package_attributes')
    difficulty_type: Mapped[Optional['DifficultyTypes']] = relationship('DifficultyTypes', back_populates='package_attributes')
    package: Mapped['Packages'] = relationship('Packages', back_populates='package_attributes')
    region: Mapped[Optional['Regions']] = relationship('Regions', back_populates='package_attributes')
    specialist: Mapped[Optional['Specialists']] = relationship('Specialists', back_populates='package_attributes')
    testimonial: Mapped[Optional['Testimonials']] = relationship('Testimonials', back_populates='package_attributes')


class PackageBookingFlightDetails(Base):
    __tablename__ = 'package_booking_flight_details'
    __table_args__ = (
        ForeignKeyConstraint(['package_booking_id'], ['package_bookings.id'], ondelete='CASCADE', name='package_booking_flight_details_package_booking_id_foreign'),
        Index('package_booking_flight_details_package_booking_id_foreign', 'package_booking_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_booking_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    arrival_date: Mapped[str] = mapped_column(String(255), nullable=False)
    arrival_time: Mapped[str] = mapped_column(String(255), nullable=False)
    arrival_flight_no: Mapped[str] = mapped_column(String(255), nullable=False)
    airport_pickup: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    departure_date: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    departure_time: Mapped[str] = mapped_column(String(255), nullable=False)
    departure_flight_no: Mapped[str] = mapped_column(String(255), nullable=False)
    airport_dropoff: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    package_booking: Mapped['PackageBookings'] = relationship('PackageBookings', back_populates='package_booking_flight_details')


class PackageBookingTravellers(Base):
    __tablename__ = 'package_booking_travellers'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='SET NULL', name='booking_traveller_countries_fk'),
        ForeignKeyConstraint(['package_booking_id'], ['package_bookings.id'], ondelete='CASCADE', name='package_booking_travellers_package_booking_id_foreign'),
        Index('booking_traveller_countries_fk', 'country_id'),
        Index('package_booking_travellers_package_booking_id_foreign', 'package_booking_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_booking_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False)
    is_leader: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('0'))
    honorific: Mapped[Optional[str]] = mapped_column(String(255))
    middle_name: Mapped[Optional[str]] = mapped_column(String(255))
    country_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    dob: Mapped[Optional[datetime.date]] = mapped_column(Date)
    passport_number: Mapped[Optional[str]] = mapped_column(String(255))
    phone_code: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    mailing_address: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_name: Mapped[Optional[str]] = mapped_column(String(255))
    relationship_: Mapped[Optional[str]] = mapped_column('relationship', String(255))
    emergency_phone: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    country: Mapped[Optional['Countries']] = relationship('Countries', back_populates='package_booking_travellers')
    package_booking: Mapped['PackageBookings'] = relationship('PackageBookings', back_populates='package_booking_travellers')


class PackageItineraryImages(Base):
    __tablename__ = 'package_itinerary_images'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='package_itinerary_images_image_id_foreign'),
        ForeignKeyConstraint(['package_itinerary_id'], ['package_itineraries.id'], ondelete='CASCADE', name='package_itinerary_images_package_itinerary_id_foreign'),
        Index('package_itinerary_images_image_id_foreign', 'image_id'),
        Index('package_itinerary_images_package_itinerary_id_foreign', 'package_itinerary_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    package_itinerary_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    display_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    image: Mapped['Images'] = relationship('Images', back_populates='package_itinerary_images')
    package_itinerary: Mapped['PackageItineraries'] = relationship('PackageItineraries', back_populates='package_itinerary_images')
