import os
import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

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

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a database session
def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()