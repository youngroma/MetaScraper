from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Upload, URL, Metadata, User
from app.utils import process_csv
from app.tasks import scrape_url
from fastapi_jwt_auth import AuthJWT
import shutil
import os

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": 'Hi there!'}

@router.post("/upload")
def upload_csv(background_tasks: BackgroundTasks, db: Session = Depends(get_db),
               file: UploadFile = File(...), Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    file_path = f"./{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload = Upload(user_id=user.id, file_name=file.filename)
    db.add(upload)
    db.commit()
    db.refresh(upload)

    # Parse CSV file and save URL to database
    urls = process_csv(file_path)
    for url in urls:
        db_url = URL(upload_id=upload.id, url=url)
        db.add(db_url)
    db.commit()

    # Run the background task for scrapping metadata
    scrape_url.delay(upload.id)  # Use the asynchronous Celery problem

    return {"message": "File uploaded successfully", "upload_id": upload.id}

@router.get("/status/{upload_id}")
def get_status(upload_id: int, db: Session = Depends(get_db)):

    urls = db.query(URL).filter(URL.upload_id == upload_id).all()
    if not urls:
        raise HTTPException(status_code=404, detail="Upload not found")

    status_summary = {"pending": 0, "success": 0, "failed": 0}
    for url in urls:
        status_summary[url.status] += 1

    return {"upload_id": upload_id, "status": status_summary}

@router.get("/results/{upload_id}")
def get_results(upload_id: int, db: Session = Depends(get_db)):

    urls = db.query(URL).filter(URL.upload_id == upload_id).all()
    if not urls:
        raise HTTPException(status_code=404, detail="Upload not found")

    results = []
    for url in urls:
        metadata = db.query(Metadata).filter(Metadata.url_id == url.id).first()
        results.append({
            "url": url.url,
            "status": url.status,
            "scraped_at": url.scraped_at,
            "title": metadata.title if metadata else None,
            "description": metadata.description if metadata else None,
            "keywords": metadata.keywords if metadata else None,
        })

    return {"upload_id": upload_id, "results": results}
