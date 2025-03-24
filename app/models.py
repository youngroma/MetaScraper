from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    uploads = relationship("Upload", back_populates="user")


class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="uploads")
    urls = relationship("URL", back_populates="upload")


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    url = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, success, failed
    scraped_at = Column(DateTime, nullable=True)

    upload = relationship("Upload", back_populates="urls")
    url_metadata = relationship("Metadata", back_populates="url", uselist=False)


class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    content = Column(Text, nullable=True)

    url = relationship("URL", back_populates="url_metadata")
