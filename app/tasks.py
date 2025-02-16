from datetime import datetime
import requests
from celery import Celery, shared_task
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import URL, Metadata
from app.utils import scrape_metadata_from_url
from worker.celery_config import celery_app


import logging
logger = logging.getLogger(__name__)

@celery_app.task
def scrape_url(upload_id: int):
    print(f"Processing upload_id={upload_id}")
    logger.info(f"Processing upload_id={upload_id}")
    db = SessionLocal()
    try:
        urls = db.query(URL).filter(URL.upload_id == upload_id, URL.status == "pending").all()
        if not urls:
            logger.info("No pending URLs found.")

        logger.info(f"Found {len(urls)} URLs to scrape.")

        for url_obj in urls:
            metadata = scrape_metadata_from_url(url_obj, db)
            if metadata:
                url_obj.status = "success"
                url_obj.scraped_at = datetime.utcnow()
            else:
                url_obj.status = "failed"
            db.commit()
    except Exception as e:
        logger.error(f"Error during scraping task {upload_id}: {e}")
    finally:
        db.close()



