from sqlalchemy.orm import Session

from models import asah_models
from schemas.scan_waste import WasteScanCreate
from datetime import datetime

def create_waste_scan(db: Session, waste: WasteScanCreate):
    """
    Create new waste scan in the database.
    """
    # create a new row in the WasteScan table
    db_waste = asah_models.ScanHistory(
        username=waste.username,
        prediction_waste=waste.prediction_waste,
        date_scan=datetime.now(),
        accuracy_percentage=waste.accuracy_percentage,
        message = waste.message,
        recycle_recommendation=waste.recycle_recommendation,
        action=waste.action,
        gcs_image_path=waste.gcs_image_path
    )
    db.add(db_waste)
    db.commit()
    db.refresh(db_waste)
    return db_waste


