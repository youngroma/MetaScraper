from datetime import datetime
import pytest
from app.database import SessionLocal
from app.models import URL, Metadata, Upload
from app.tasks import scrape_url
from app.utils import scrape_metadata_from_url

@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

def test_scrape_url(db):
    upload = Upload(id=9992, user_id=1, file_name="test_file1.csv", uploaded_at=datetime.utcnow())
    db.add(upload)
    db.commit()

    url = URL(upload_id=9992, url="https://www.apple.com/mac/", status="pending")
    db.add(url)
    db.commit()

    scrape_url(url.upload_id)

    metadata = db.query(Metadata).filter(Metadata.url_id == url.id).first()

    assert metadata is not None, "Metadata not preserved!"

    print("Test passed!")

