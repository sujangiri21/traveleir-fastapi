from typing import Optional
import datetime
import decimal
import enum

from sqlalchemy import CHAR, Column, Computed, DECIMAL, Date, Double, Enum, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
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


class FailedJobs(Base):
    __tablename__ = 'failed_jobs'

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    connection: Mapped[str] = mapped_column(Text, nullable=False)
    queue: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    exception: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    failed_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('current_timestamp()'))


class Jobs(Base):
    __tablename__ = 'jobs'
    __table_args__ = (
        Index('jobs_queue_index', 'queue'),
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    queue: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    attempts: Mapped[int] = mapped_column(TINYINT(3, unsigned=True), nullable=False)
    available_at: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)
    created_at: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)
    reserved_at: Mapped[Optional[int]] = mapped_column(INTEGER(10, unsigned=True))


class Migrations(Base):
    __tablename__ = 'migrations'

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True)
    migration: Mapped[str] = mapped_column(String(255), nullable=False)
    batch: Mapped[int] = mapped_column(INTEGER(11), nullable=False)


class PasswordResets(Base):
    __tablename__ = 'password_resets'
    __table_args__ = (
        Index('password_resets_email_index', 'email'),
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)


class Permissions(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        Index('permissions_code_unique', 'code', unique=True),
        Index('permissions_name_unique', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    group: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    user_type: Mapped[list['UserTypes']] = relationship('UserTypes', secondary='user_type_permission', back_populates='permission')


class PersonalAccessTokens(Base):
    __tablename__ = 'personal_access_tokens'
    __table_args__ = (
        Index('personal_access_tokens_token_unique', 'token', unique=True),
        Index('personal_access_tokens_tokenable_type_tokenable_id_index', 'tokenable_type', 'tokenable_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    tokenable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    tokenable_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str] = mapped_column(String(64), nullable=False)
    abilities: Mapped[Optional[str]] = mapped_column(Text)
    last_used_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)


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
    role_permissions: Mapped[list['RolePermissions']] = relationship('RolePermissions', back_populates='role')


class SearchLogs(Base):
    __tablename__ = 'search_logs'

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    result_count: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, server_default=text('0'))
    has_results: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('0'))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    session_id: Mapped[Optional[str]] = mapped_column(String(255))
    user_agent: Mapped[Optional[str]] = mapped_column(String(255))
    search: Mapped[Optional[str]] = mapped_column(String(255))
    filters: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    results: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    match_location: Mapped[Optional[str]] = mapped_column(String(255))
    match_location_type: Mapped[Optional[str]] = mapped_column(String(255))
    currency: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)


class SectionConfigs(Base):
    __tablename__ = 'section_configs'

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    section_name: Mapped[str] = mapped_column(String(255), nullable=False)
    section_index: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    section_filename: Mapped[str] = mapped_column(String(100), nullable=False)
    has_title: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    has_subtitle: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    has_description: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    has_image: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    has_slider: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    has_link: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    has_video: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    has_list: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    no_of_images: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    no_of_sliders: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    no_of_videos: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    has_type: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    list_config_heads: Mapped[list['ListConfigHeads']] = relationship('ListConfigHeads', back_populates='config')
    type_configs: Mapped[list['TypeConfigs']] = relationship('TypeConfigs', back_populates='config')
    list_config_bodies: Mapped[list['ListConfigBodies']] = relationship('ListConfigBodies', back_populates='config')
    section_contents: Mapped[list['SectionContents']] = relationship('SectionContents', back_populates='config')


class Sessions(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        Index('sessions_last_activity_index', 'last_activity'),
        Index('sessions_session_id_unique', 'session_id', unique=True),
        Index('sessions_user_id_index', 'user_id')
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    last_activity: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)


class TailorMadePackages(Base):
    __tablename__ = 'tailor_made_packages'

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(32))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    value1: Mapped[Optional[str]] = mapped_column(Text)
    value2: Mapped[Optional[str]] = mapped_column(Text)
    value3: Mapped[Optional[str]] = mapped_column(Text)
    value4: Mapped[Optional[str]] = mapped_column(Text)
    value5: Mapped[Optional[str]] = mapped_column(Text)
    value6: Mapped[Optional[str]] = mapped_column(Text)
    value7: Mapped[Optional[str]] = mapped_column(Text)
    value8: Mapped[Optional[str]] = mapped_column(Text)
    value9: Mapped[Optional[str]] = mapped_column(Text)
    value10: Mapped[Optional[str]] = mapped_column(Text)
    message: Mapped[Optional[str]] = mapped_column(Text)
    is_reviewed: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)


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
    trip_agent_seos: Mapped[list['TripAgentSeos']] = relationship('TripAgentSeos', back_populates='trip_agent')


class UserTypes(Base):
    __tablename__ = 'user_types'

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    permission: Mapped[list['Permissions']] = relationship('Permissions', secondary='user_type_permission', back_populates='user_type')
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
    list_groups: Mapped[list['ListGroups']] = relationship('ListGroups', back_populates='user')
    meal_plans: Mapped[list['MealPlans']] = relationship('MealPlans', back_populates='user')
    page_configs: Mapped[list['PageConfigs']] = relationship('PageConfigs', back_populates='user')
    pages: Mapped[list['Pages']] = relationship('Pages', back_populates='user')
    section_config_builds: Mapped[list['SectionConfigBuilds']] = relationship('SectionConfigBuilds', back_populates='user')
    settings: Mapped[list['Settings']] = relationship('Settings', back_populates='user')
    sliders: Mapped[list['Sliders']] = relationship('Sliders', back_populates='user')
    trip_addons: Mapped[list['TripAddons']] = relationship('TripAddons', back_populates='user')
    user_permissions: Mapped[list['UserPermissions']] = relationship('UserPermissions', back_populates='user')
    activities: Mapped[list['Activities']] = relationship('Activities', back_populates='user')
    countries: Mapped[list['Countries']] = relationship('Countries', back_populates='user')
    destinations: Mapped[list['Destinations']] = relationship('Destinations', back_populates='user')
    difficulty_types: Mapped[list['DifficultyTypes']] = relationship('DifficultyTypes', back_populates='user')
    hotels: Mapped[list['Hotels']] = relationship('Hotels', back_populates='user')
    popups: Mapped[list['Popups']] = relationship('Popups', back_populates='user')
    restaurants: Mapped[list['Restaurants']] = relationship('Restaurants', back_populates='user')
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
    image_list_content_bodies: Mapped[list['ImageListContentBodies']] = relationship('ImageListContentBodies', back_populates='image')
    image_list_content_heads: Mapped[list['ImageListContentHeads']] = relationship('ImageListContentHeads', back_populates='image')
    media_usage: Mapped[list['MediaUsage']] = relationship('MediaUsage', back_populates='media')
    package_images: Mapped[list['PackageImages']] = relationship('PackageImages', back_populates='image')
    package_map_images: Mapped[list['PackageMapImages']] = relationship('PackageMapImages', back_populates='image')
    package_maps: Mapped[list['PackageMaps']] = relationship('PackageMaps', back_populates='image')
    package_seos: Mapped[list['PackageSeos']] = relationship('PackageSeos', back_populates='image')
    package_videos: Mapped[list['PackageVideos']] = relationship('PackageVideos', back_populates='image')
    page_seos: Mapped[list['PageSeos']] = relationship('PageSeos', back_populates='image')
    popups: Mapped[list['Popups']] = relationship('Popups', back_populates='image')
    restaurants: Mapped[list['Restaurants']] = relationship('Restaurants', back_populates='image')
    slider_items: Mapped[list['SliderItems']] = relationship('SliderItems', back_populates='image')
    specialists: Mapped[list['Specialists']] = relationship('Specialists', back_populates='image')
    trip_agent_seos: Mapped[list['TripAgentSeos']] = relationship('TripAgentSeos', back_populates='image')
    image_contents: Mapped[list['ImageContents']] = relationship('ImageContents', back_populates='image')
    regions: Mapped[list['Regions']] = relationship('Regions', back_populates='image')
    package_itinerary_images: Mapped[list['PackageItineraryImages']] = relationship('PackageItineraryImages', back_populates='image')


class ListConfigHeads(Base):
    __tablename__ = 'list_config_heads'
    __table_args__ = (
        ForeignKeyConstraint(['config_id'], ['section_configs.id'], ondelete='CASCADE', name='list_config_heads_config_id_foreign'),
        Index('list_config_heads_config_id_foreign', 'config_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    has_title: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_subtitle: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_description: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_image: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_link: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    no_of_images: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    config_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)

    config: Mapped['SectionConfigs'] = relationship('SectionConfigs', back_populates='list_config_heads')
    list_config_bodies: Mapped[list['ListConfigBodies']] = relationship('ListConfigBodies', back_populates='head')
    list_content_heads: Mapped[list['ListContentHeads']] = relationship('ListContentHeads', back_populates='list_config')


class ListGroups(Base):
    __tablename__ = 'list_groups'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='list_groups_user_id_foreign'),
        Index('list_groups_name_unique', 'name', unique=True),
        Index('list_groups_slug_unique', 'slug', unique=True),
        Index('list_groups_user_id_foreign', 'user_id'),
        Index('list_groups_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    list_type: Mapped[str] = mapped_column(String(32), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    items: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='list_groups')


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


class PageConfigs(Base):
    __tablename__ = 'page_configs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='page_configs_user_id_foreign'),
        Index('page_configs_user_id_foreign', 'user_id'),
        Index('page_configs_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sections: Mapped[str] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    header_id: Mapped[Optional[int]] = mapped_column(TINYINT(4))
    footer_id: Mapped[Optional[int]] = mapped_column(TINYINT(4))
    is_preset: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='page_configs')


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
    page_seos: Mapped[list['PageSeos']] = relationship('PageSeos', back_populates='page')
    restaurants: Mapped[list['Restaurants']] = relationship('Restaurants', back_populates='page')
    section_contents: Mapped[list['SectionContents']] = relationship('SectionContents', back_populates='page')
    web_alias: Mapped[list['WebAlias']] = relationship('WebAlias', back_populates='page')
    popup_pages: Mapped[list['PopupPages']] = relationship('PopupPages', back_populates='page')
    regions: Mapped[list['Regions']] = relationship('Regions', back_populates='page')


class RolePermissions(Base):
    __tablename__ = 'role_permissions'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='role_permissions_role_id_foreign'),
        Index('role_permissions_role_id_foreign', 'role_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    role_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    permission_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    role: Mapped['Roles'] = relationship('Roles', back_populates='role_permissions')


class SectionConfigBuilds(Base):
    __tablename__ = 'section_config_builds'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='section_config_builds_user_id_foreign'),
        Index('section_config_builds_filename_unique', 'filename', unique=True),
        Index('section_config_builds_user_id_foreign', 'user_id'),
        Index('section_config_builds_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    filename: Mapped[str] = mapped_column(String(100), nullable=False)
    config: Mapped[str] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=False)
    display_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    list_config: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    type_config: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    styles: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    scripts: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='section_config_builds')


class Settings(Base):
    __tablename__ = 'settings'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='settings_user_id_foreign'),
        Index('settings_name_unique', 'name', unique=True),
        Index('settings_slug_unique', 'slug', unique=True),
        Index('settings_user_id_foreign', 'user_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    value: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='settings')


class Sliders(Base):
    __tablename__ = 'sliders'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='sliders_user_id_foreign'),
        Index('sliders_name_unique', 'name', unique=True),
        Index('sliders_user_id_foreign', 'user_id'),
        Index('sliders_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='sliders')
    slider_items: Mapped[list['SliderItems']] = relationship('SliderItems', back_populates='slider')
    slider_contents: Mapped[list['SliderContents']] = relationship('SliderContents', back_populates='slider')


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


class TypeConfigs(Base):
    __tablename__ = 'type_configs'
    __table_args__ = (
        ForeignKeyConstraint(['config_id'], ['section_configs.id'], ondelete='CASCADE', name='type_configs_config_id_foreign'),
        Index('type_configs_config_id_foreign', 'config_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    config_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    type_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)

    config: Mapped['SectionConfigs'] = relationship('SectionConfigs', back_populates='type_configs')


class UserPermissions(Base):
    __tablename__ = 'user_permissions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_permissions_user_id_foreign'),
        Index('user_permissions_user_id_foreign', 'user_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    permission_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='user_permissions')


t_user_type_permission = Table(
    'user_type_permission', Base.metadata,
    Column('user_type_id', BIGINT(20, unsigned=True), nullable=False),
    Column('permission_id', BIGINT(20, unsigned=True), nullable=False),
    ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE', name='user_type_permission_permission_id_foreign'),
    ForeignKeyConstraint(['user_type_id'], ['user_types.id'], ondelete='CASCADE', name='user_type_permission_user_type_id_foreign'),
    Index('user_type_permission_permission_id_foreign', 'permission_id'),
    Index('user_type_permission_user_type_id_foreign', 'user_type_id')
)


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
    activity_destinations: Mapped[list['ActivityDestinations']] = relationship('ActivityDestinations', back_populates='activity')
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
    activity_destinations: Mapped[list['ActivityDestinations']] = relationship('ActivityDestinations', back_populates='destination')
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


class ImageListContentBodies(Base):
    __tablename__ = 'image_list_content_bodies'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='image_list_content_bodies_image_id_foreign'),
        Index('image_list_content_bodies_image_id_foreign', 'image_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    list_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)
    display_order: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    image: Mapped['Images'] = relationship('Images', back_populates='image_list_content_bodies')


class ImageListContentHeads(Base):
    __tablename__ = 'image_list_content_heads'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='image_list_content_heads_image_id_foreign'),
        Index('image_list_content_heads_image_id_foreign', 'image_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    list_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)
    display_order: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    image: Mapped['Images'] = relationship('Images', back_populates='image_list_content_heads')


class ListConfigBodies(Base):
    __tablename__ = 'list_config_bodies'
    __table_args__ = (
        ForeignKeyConstraint(['config_id'], ['section_configs.id'], ondelete='CASCADE', name='list_config_bodies_config_id_foreign'),
        ForeignKeyConstraint(['head_id'], ['list_config_heads.id'], ondelete='CASCADE', name='list_config_bodies_head_id_foreign'),
        Index('list_config_bodies_config_id_foreign', 'config_id'),
        Index('list_config_bodies_head_id_foreign', 'head_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    has_title: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_subtitle: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_description: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_image: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_link: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    has_icon: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    no_of_images: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    head_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    config_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)

    config: Mapped['SectionConfigs'] = relationship('SectionConfigs', back_populates='list_config_bodies')
    head: Mapped['ListConfigHeads'] = relationship('ListConfigHeads', back_populates='list_config_bodies')
    list_content_bodies: Mapped[list['ListContentBodies']] = relationship('ListContentBodies', back_populates='list_config')


class MediaUsage(Base):
    __tablename__ = 'media_usage'
    __table_args__ = (
        ForeignKeyConstraint(['media_id'], ['images.id'], ondelete='CASCADE', name='media_usage_media_id_foreign'),
        Index('media_usage_media_id_foreign', 'media_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    media_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    resource_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(255), nullable=False)
    display_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'))
    type: Mapped[Optional[str]] = mapped_column(String(255))
    tag: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    media: Mapped['Images'] = relationship('Images', back_populates='media_usage')


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


class PageSeos(Base):
    __tablename__ = 'page_seos'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='page_seos_image_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='CASCADE', name='page_seos_page_id_foreign'),
        Index('page_seos_image_id_foreign', 'image_id'),
        Index('page_seos_page_id_foreign', 'page_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    page_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    meta_title: Mapped[str] = mapped_column(Text, nullable=False)
    meta_description: Mapped[str] = mapped_column(Text, nullable=False)
    meta_keywords: Mapped[str] = mapped_column(Text, nullable=False)
    image_alt: Mapped[Optional[str]] = mapped_column(Text)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='page_seos')
    page: Mapped['Pages'] = relationship('Pages', back_populates='page_seos')


class Popups(Base):
    __tablename__ = 'popups'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='popups_image_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='popups_user_id_foreign'),
        Index('popups_image_id_foreign', 'image_id'),
        Index('popups_user_id_foreign', 'user_id'),
        Index('popups_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    video_link: Mapped[Optional[str]] = mapped_column(Text)
    external_link: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    image: Mapped['Images'] = relationship('Images', back_populates='popups')
    user: Mapped['Users'] = relationship('Users', back_populates='popups')
    popup_pages: Mapped[list['PopupPages']] = relationship('PopupPages', back_populates='popup')


class Restaurants(Base):
    __tablename__ = 'restaurants'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='restaurants_image_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='SET NULL', name='restaurants_page_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='restaurants_user_id_foreign'),
        Index('restaurants_image_id_foreign', 'image_id'),
        Index('restaurants_name_unique', 'name', unique=True),
        Index('restaurants_page_id_foreign', 'page_id'),
        Index('restaurants_user_id_foreign', 'user_id'),
        Index('restaurants_uuid_unique', 'uuid', unique=True)
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

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='restaurants')
    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='restaurants')
    user: Mapped['Users'] = relationship('Users', back_populates='restaurants')


class SectionContents(Base):
    __tablename__ = 'section_contents'
    __table_args__ = (
        ForeignKeyConstraint(['config_id'], ['section_configs.id'], ondelete='CASCADE', name='section_contents_config_id_foreign'),
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='CASCADE', name='section_contents_page_id_foreign'),
        Index('section_contents_config_id_foreign', 'config_id'),
        Index('section_contents_page_id_foreign', 'page_id'),
        Index('section_contents_uuid_unique', 'uuid', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    section_name: Mapped[str] = mapped_column(String(255), nullable=False)
    uuid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    page_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    config_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text)
    subtitle: Mapped[Optional[str]] = mapped_column(Text)
    display_order: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    config: Mapped['SectionConfigs'] = relationship('SectionConfigs', back_populates='section_contents')
    page: Mapped['Pages'] = relationship('Pages', back_populates='section_contents')
    image_contents: Mapped[list['ImageContents']] = relationship('ImageContents', back_populates='section')
    list_content_heads: Mapped[list['ListContentHeads']] = relationship('ListContentHeads', back_populates='section')
    list_links: Mapped[list['ListLinks']] = relationship('ListLinks', back_populates='section')
    list_videos: Mapped[list['ListVideos']] = relationship('ListVideos', back_populates='section')
    section_descriptions: Mapped[list['SectionDescriptions']] = relationship('SectionDescriptions', back_populates='section')
    slider_contents: Mapped[list['SliderContents']] = relationship('SliderContents', back_populates='section')
    type_contents: Mapped[list['TypeContents']] = relationship('TypeContents', back_populates='section')
    list_content_bodies: Mapped[list['ListContentBodies']] = relationship('ListContentBodies', back_populates='section')


class SliderItems(Base):
    __tablename__ = 'slider_items'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='slider_items_image_id_foreign'),
        ForeignKeyConstraint(['slider_id'], ['sliders.id'], name='slider_items_slider_id_foreign'),
        Index('slider_items_image_id_foreign', 'image_id'),
        Index('slider_items_slider_id_foreign', 'slider_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    slider_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    display_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    display_type: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    link: Mapped[Optional[str]] = mapped_column(Text)
    video_url: Mapped[Optional[str]] = mapped_column(String(255))
    image_title: Mapped[Optional[str]] = mapped_column(String(255))
    image_caption: Mapped[Optional[str]] = mapped_column(String(255))

    image: Mapped['Images'] = relationship('Images', back_populates='slider_items')
    slider: Mapped['Sliders'] = relationship('Sliders', back_populates='slider_items')


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


class TripAgentSeos(Base):
    __tablename__ = 'trip_agent_seos'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='SET NULL', name='trip_agent_seos_image_id_foreign'),
        ForeignKeyConstraint(['trip_agent_id'], ['trip_agents.id'], ondelete='CASCADE', name='trip_agent_seos_trip_agent_id_foreign'),
        Index('trip_agent_seos_image_id_foreign', 'image_id'),
        Index('trip_agent_seos_trip_agent_id_foreign', 'trip_agent_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    trip_agent_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    meta_title: Mapped[str] = mapped_column(Text, nullable=False)
    meta_description: Mapped[str] = mapped_column(Text, nullable=False)
    meta_keywords: Mapped[str] = mapped_column(Text, nullable=False)
    image_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    image_alt: Mapped[Optional[str]] = mapped_column(Text)

    image: Mapped[Optional['Images']] = relationship('Images', back_populates='trip_agent_seos')
    trip_agent: Mapped['TripAgents'] = relationship('TripAgents', back_populates='trip_agent_seos')


class WebAlias(Base):
    __tablename__ = 'web_alias'
    __table_args__ = (
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='CASCADE', name='web_alias_page_id_foreign'),
        Index('web_alias_alias_unique', 'alias', unique=True),
        Index('web_alias_page_id_foreign', 'page_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    alias: Mapped[str] = mapped_column(String(255), nullable=False)
    page_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    news_id: Mapped[Optional[int]] = mapped_column(INTEGER(10, unsigned=True))
    event_id: Mapped[Optional[int]] = mapped_column(INTEGER(10, unsigned=True))
    package_id: Mapped[Optional[int]] = mapped_column(INTEGER(10, unsigned=True))
    old_url: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))

    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='web_alias')


class ActivityDestinations(Base):
    __tablename__ = 'activity_destinations'
    __table_args__ = (
        ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='CASCADE', name='activity_destinations_activity_id_foreign'),
        ForeignKeyConstraint(['destination_id'], ['destinations.id'], ondelete='CASCADE', name='activity_destinations_destination_id_foreign'),
        Index('activity_destinations_activity_id_foreign', 'activity_id'),
        Index('activity_destinations_destination_id_foreign', 'destination_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    activity_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    destination_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)

    activity: Mapped['Activities'] = relationship('Activities', back_populates='activity_destinations')
    destination: Mapped['Destinations'] = relationship('Destinations', back_populates='activity_destinations')


class ImageContents(Base):
    __tablename__ = 'image_contents'
    __table_args__ = (
        ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE', name='image_contents_image_id_foreign'),
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='image_contents_section_id_foreign'),
        Index('image_contents_image_id_foreign', 'image_id'),
        Index('image_contents_section_id_foreign', 'section_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    image_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    display_order: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    image: Mapped['Images'] = relationship('Images', back_populates='image_contents')
    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='image_contents')


class ListContentHeads(Base):
    __tablename__ = 'list_content_heads'
    __table_args__ = (
        ForeignKeyConstraint(['list_config_id'], ['list_config_heads.id'], ondelete='CASCADE', name='list_content_heads_list_config_id_foreign'),
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='list_content_heads_section_id_foreign'),
        Index('list_content_heads_list_config_id_foreign', 'list_config_id'),
        Index('list_content_heads_section_id_foreign', 'section_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    list_config_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    target: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'_self'"))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    subtitle: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    link_title: Mapped[Optional[str]] = mapped_column(String(255))
    link: Mapped[Optional[str]] = mapped_column(String(255))

    list_config: Mapped['ListConfigHeads'] = relationship('ListConfigHeads', back_populates='list_content_heads')
    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='list_content_heads')
    list_content_bodies: Mapped[list['ListContentBodies']] = relationship('ListContentBodies', back_populates='head')


class ListLinks(Base):
    __tablename__ = 'list_links'
    __table_args__ = (
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='list_links_section_id_foreign'),
        Index('list_links_section_id_foreign', 'section_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    target: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'_self'"))
    display_type: Mapped[int] = mapped_column(TINYINT(4), nullable=False)
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    display_order: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='list_links')


class ListVideos(Base):
    __tablename__ = 'list_videos'
    __table_args__ = (
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='list_videos_section_id_foreign'),
        Index('list_videos_section_id_foreign', 'section_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    target: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'_self'"))
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    video_thumbnail_id: Mapped[Optional[int]] = mapped_column(INTEGER(10, unsigned=True))

    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='list_videos')


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


class PopupPages(Base):
    __tablename__ = 'popup_pages'
    __table_args__ = (
        ForeignKeyConstraint(['page_id'], ['pages.id'], ondelete='CASCADE', name='popup_pages_page_id_foreign'),
        ForeignKeyConstraint(['popup_id'], ['popups.id'], name='popup_pages_popup_id_foreign'),
        Index('popup_pages_page_id_foreign', 'page_id'),
        Index('popup_pages_popup_id_foreign', 'popup_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    popup_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    page_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))

    page: Mapped[Optional['Pages']] = relationship('Pages', back_populates='popup_pages')
    popup: Mapped['Popups'] = relationship('Popups', back_populates='popup_pages')


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


class SectionDescriptions(Base):
    __tablename__ = 'section_descriptions'
    __table_args__ = (
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='section_descriptions_section_id_foreign'),
        Index('section_descriptions_section_id_foreign', 'section_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='section_descriptions')


class SliderContents(Base):
    __tablename__ = 'slider_contents'
    __table_args__ = (
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='slider_contents_section_id_foreign'),
        ForeignKeyConstraint(['slider_id'], ['sliders.id'], name='slider_contents_slider_id_foreign'),
        Index('slider_contents_section_id_foreign', 'section_id'),
        Index('slider_contents_slider_id_foreign', 'slider_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    slider_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)

    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='slider_contents')
    slider: Mapped['Sliders'] = relationship('Sliders', back_populates='slider_contents')


class TypeContents(Base):
    __tablename__ = 'type_contents'
    __table_args__ = (
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='type_contents_section_id_foreign'),
        Index('type_contents_section_id_foreign', 'section_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    item_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)
    type_config_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    display_order: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)

    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='type_contents')


class ListContentBodies(Base):
    __tablename__ = 'list_content_bodies'
    __table_args__ = (
        ForeignKeyConstraint(['head_id'], ['list_content_heads.id'], ondelete='CASCADE', name='list_content_bodies_head_id_foreign'),
        ForeignKeyConstraint(['list_config_id'], ['list_config_bodies.id'], ondelete='CASCADE', name='list_content_bodies_list_config_id_foreign'),
        ForeignKeyConstraint(['section_id'], ['section_contents.id'], ondelete='CASCADE', name='list_content_bodies_section_id_foreign'),
        Index('list_content_bodies_head_id_foreign', 'head_id'),
        Index('list_content_bodies_list_config_id_foreign', 'list_config_id'),
        Index('list_content_bodies_section_id_foreign', 'section_id')
    )

    id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), primary_key=True)
    group_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False)
    list_config_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    section_id: Mapped[int] = mapped_column(BIGINT(20, unsigned=True), nullable=False)
    target: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'_self'"))
    head_id: Mapped[Optional[int]] = mapped_column(BIGINT(20, unsigned=True))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    subtitle: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    icon: Mapped[Optional[str]] = mapped_column(String(255))
    link_title: Mapped[Optional[str]] = mapped_column(String(255))
    link: Mapped[Optional[str]] = mapped_column(String(255))
    display_order: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    head: Mapped[Optional['ListContentHeads']] = relationship('ListContentHeads', back_populates='list_content_bodies')
    list_config: Mapped['ListConfigBodies'] = relationship('ListConfigBodies', back_populates='list_content_bodies')
    section: Mapped['SectionContents'] = relationship('SectionContents', back_populates='list_content_bodies')


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
