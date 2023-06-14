from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from models import asah_models
from schemas.scan_waste import WasteScanCreate
from fastapi import HTTPException

def get_scan_history(db: Session, username: str):
    """
    Retrieve scan history for a user.
    """
    scans = db.query(asah_models.ScanHistory).filter(asah_models.ScanHistory.username == username).all()
    return scans

def get_scan(username: str, waste_id: str, db: Session):
    return db.query(asah_models.ScanHistory).filter(asah_models.ScanHistory.username == username, asah_models.ScanHistory.waste_id == waste_id).first()

def delete_scan(username: str, waste_id: str, db: Session):
    scan = get_scan(username, waste_id, db)
    if scan:
        db.delete(scan)
        db.commit()
        return {"message": "successfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="Scan not found")