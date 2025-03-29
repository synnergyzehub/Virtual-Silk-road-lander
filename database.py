import os
import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Date, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import json

# Get the database connection URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    # Fallback to SQLite for development
    DATABASE_URL = "sqlite:///voi_jeans.db"

# Create the SQLAlchemy engine with connection pooling settings
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"connect_timeout": 15}
)

# Create a base class for declarative models
Base = declarative_base()

# Define the models for our manufacturing lifecycle management system
class Buyer(Base):
    __tablename__ = 'buyers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="buyer")
    
    def __repr__(self):
        return f"<Buyer(name='{self.name}')>"

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    po_number = Column(String(50), nullable=False, unique=True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)
    status = Column(String(20), default='New')  # New, In Progress, Completed, Cancelled
    total_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    buyer = relationship("Buyer", back_populates="orders")
    styles = relationship("Style", back_populates="order")
    
    def __repr__(self):
        return f"<Order(po_number='{self.po_number}', status='{self.status}')>"

class Style(Base):
    __tablename__ = 'styles'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    style_number = Column(String(50), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # T-shirt, Pants, Jacket, etc.
    color = Column(String(50))
    size_breakdown = Column(Text)  # JSON string of size breakdown
    quantity = Column(Integer, default=0)
    status = Column(String(20), default='New')  # New, In Progress, Completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="styles")
    materials = relationship("Material", back_populates="style")
    production_entries = relationship("ProductionEntry", back_populates="style")
    line_allocations = relationship("LineAllocation", back_populates="style")
    
    def __repr__(self):
        return f"<Style(style_number='{self.style_number}', quantity={self.quantity})>"

class Material(Base):
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True)
    style_id = Column(Integer, ForeignKey('styles.id'))
    name = Column(String(100), nullable=False)
    type = Column(String(50))  # Fabric, Trim, Accessories
    unit = Column(String(20))  # Meters, Pieces, etc.
    required_quantity = Column(Float, default=0.0)
    received_quantity = Column(Float, default=0.0)
    issued_quantity = Column(Float, default=0.0)
    status = Column(String(20), default='Pending')  # Pending, Ordered, Received, Issued
    po_number = Column(String(50))  # Material purchase order number
    po_date = Column(Date)
    expected_delivery = Column(Date)
    actual_delivery = Column(Date)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    style = relationship("Style", back_populates="materials")
    
    def __repr__(self):
        return f"<Material(name='{self.name}', status='{self.status}')>"

class ProductionLine(Base):
    __tablename__ = 'production_lines'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer)  # Pieces per day
    active = Column(Boolean, default=True)
    supervisor = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    line_allocations = relationship("LineAllocation", back_populates="line")
    production_entries = relationship("ProductionEntry", back_populates="line")
    
    def __repr__(self):
        return f"<ProductionLine(name='{self.name}', capacity={self.capacity})>"

class LineAllocation(Base):
    __tablename__ = 'line_allocations'
    
    id = Column(Integer, primary_key=True)
    line_id = Column(Integer, ForeignKey('production_lines.id'))
    style_id = Column(Integer, ForeignKey('styles.id'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    planned_quantity = Column(Integer, default=0)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    line = relationship("ProductionLine", back_populates="line_allocations")
    style = relationship("Style", back_populates="line_allocations")
    
    def __repr__(self):
        return f"<LineAllocation(line='{self.line.name}', style='{self.style.style_number}')>"

class ProductionEntry(Base):
    __tablename__ = 'production_entries'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    style_id = Column(Integer, ForeignKey('styles.id'))
    line_id = Column(Integer, ForeignKey('production_lines.id'))
    process = Column(String(20))  # Cutting, Stitching, Packing, Dispatch
    quantity = Column(Integer, default=0)
    efficiency = Column(Float, default=0.0)  # Percentage
    defects = Column(Integer, default=0)
    delay_reason = Column(Text)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    style = relationship("Style", back_populates="production_entries")
    line = relationship("ProductionLine", back_populates="production_entries")
    
    def __repr__(self):
        return f"<ProductionEntry(date='{self.date}', process='{self.process}', quantity={self.quantity})>"

# Create all tables in the database
def create_tables():
    Base.metadata.create_all(engine)

# Empire OS Models for Data Sharing and License Management
class EmpireEntity(Base):
    __tablename__ = 'empire_entities'
    
    id = Column(Integer, primary_key=True)
    eip_id = Column(String(50), unique=True, nullable=False)  # EIP = Empire Identity Protocol
    name = Column(String(100), nullable=False)
    entity_type = Column(String(50))  # Company, Individual, etc.
    business_type = Column(String(50))  # Manufacturer, Retailer, Brand
    country = Column(String(50))
    registration_id = Column(String(100))  # GST/PAN/CIN
    mobile_number = Column(String(20))
    status = Column(String(20), default='Pending')  # Pending, Active, Rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    business_models = relationship("EntityBusinessModel", back_populates="entity")
    data_sharing_agreements = relationship("DataSharingAgreement", back_populates="entity")
    license_grants = relationship("LicenseGrant", back_populates="entity")
    
    def __repr__(self):
        return f"<EmpireEntity(name='{self.name}', eip_id='{self.eip_id}', business_type='{self.business_type}')>"

class BusinessModelMaster(Base):
    __tablename__ = 'business_model_master'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)  # CMP, FOB, SOR, etc.
    name = Column(String(100), nullable=False)
    description = Column(Text)
    business_type = Column(String(50), nullable=False)  # Manufacturer, Retailer, Brand
    network = Column(String(50))  # Woven Supply, Commune Connect, Both
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    entity_models = relationship("EntityBusinessModel", back_populates="business_model")
    modules = relationship("BusinessModelModule", back_populates="business_model")
    
    def __repr__(self):
        return f"<BusinessModelMaster(code='{self.code}', name='{self.name}')>"

class ModuleMaster(Base):
    __tablename__ = 'module_master'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # Production, Retail, Analytics, etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    business_model_modules = relationship("BusinessModelModule", back_populates="module")
    
    def __repr__(self):
        return f"<ModuleMaster(code='{self.code}', name='{self.name}')>"

class BusinessModelModule(Base):
    __tablename__ = 'business_model_modules'
    
    id = Column(Integer, primary_key=True)
    business_model_id = Column(Integer, ForeignKey('business_model_master.id'))
    module_id = Column(Integer, ForeignKey('module_master.id'))
    is_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    business_model = relationship("BusinessModelMaster", back_populates="modules")
    module = relationship("ModuleMaster", back_populates="business_model_modules")
    
    def __repr__(self):
        return f"<BusinessModelModule(business_model='{self.business_model.code}', module='{self.module.code}')>"

class EntityBusinessModel(Base):
    __tablename__ = 'entity_business_models'
    
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('empire_entities.id'))
    business_model_id = Column(Integer, ForeignKey('business_model_master.id'))
    status = Column(String(20), default='Active')  # Active, Inactive, Suspended
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    entity = relationship("EmpireEntity", back_populates="business_models")
    business_model = relationship("BusinessModelMaster", back_populates="entity_models")
    
    def __repr__(self):
        return f"<EntityBusinessModel(entity='{self.entity.name}', business_model='{self.business_model.code}')>"

class LicenseTemplate(Base):
    __tablename__ = 'license_templates'
    
    id = Column(Integer, primary_key=True)
    template_id = Column(String(50), unique=True, nullable=False)  # e.g., TEMPLATE-CMP-001
    name = Column(String(100), nullable=False)
    business_type = Column(String(50), nullable=False)  # Manufacturer, Retailer, Brand
    business_model_code = Column(String(20), nullable=False)  # CMP, FOB, SOR, etc.
    description = Column(Text)
    terms = Column(Text)  # Terms and conditions
    data_access_level = Column(String(20))  # Full, Limited, Restricted
    validity_days = Column(Integer, default=365)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    license_grants = relationship("LicenseGrant", back_populates="license_template")
    
    def __repr__(self):
        return f"<LicenseTemplate(template_id='{self.template_id}', name='{self.name}')>"

class LicenseGrant(Base):
    __tablename__ = 'license_grants'
    
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('empire_entities.id'))
    license_template_id = Column(Integer, ForeignKey('license_templates.id'))
    license_key = Column(String(100), unique=True, nullable=False)
    granted_date = Column(DateTime, default=datetime.datetime.utcnow)
    expiry_date = Column(DateTime)
    status = Column(String(20), default='Active')  # Active, Expired, Revoked, Suspended
    notes = Column(Text)
    
    # Relationships
    entity = relationship("EmpireEntity", back_populates="license_grants")
    license_template = relationship("LicenseTemplate", back_populates="license_grants")
    
    def __repr__(self):
        return f"<LicenseGrant(entity='{self.entity.name}', license_key='{self.license_key}', status='{self.status}')>"

class DataSharingAgreement(Base):
    __tablename__ = 'data_sharing_agreements'
    
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('empire_entities.id'))
    agreement_ref = Column(String(50), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    version = Column(String(20), default='1.0')
    signed_date = Column(DateTime)
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime)
    status = Column(String(20), default='Draft')  # Draft, Active, Expired, Terminated
    agreement_text = Column(Text)
    sharing_scope = Column(JSON)  # JSON object defining data sharing scope
    restrictions = Column(JSON)  # JSON object defining usage restrictions
    governance_rules = Column(JSON)  # JSON object defining governance rules
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    entity = relationship("EmpireEntity", back_populates="data_sharing_agreements")
    
    def __repr__(self):
        return f"<DataSharingAgreement(entity='{self.entity.name}', agreement_ref='{self.agreement_ref}', status='{self.status}')>"

class RiverTransaction(Base):
    __tablename__ = 'river_transactions'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(100), unique=True, nullable=False)
    entity_id = Column(Integer, ForeignKey('empire_entities.id'))
    transaction_type = Column(String(50))  # Data Access, License Grant, Data Sharing, etc.
    resource_type = Column(String(50))  # Order, Style, Material, etc.
    resource_id = Column(String(50))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    access_level = Column(String(20))  # Read, Write, Full
    status = Column(String(20))  # Success, Failed, Pending
    details = Column(JSON)  # Additional transaction details
    
    def __repr__(self):
        return f"<RiverTransaction(transaction_id='{self.transaction_id}', transaction_type='{self.transaction_type}')>"

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a database session
def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()