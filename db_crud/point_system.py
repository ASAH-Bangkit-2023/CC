from sqlalchemy.orm import Session
from models.asah_models import PointSystem
from schemas.point_system import PointSystemCreate

def create_point_system(db: Session, point_system_data: PointSystemCreate) -> PointSystem:
    # Membuat objek PointSystem dari data yang diterima
    point_system = PointSystem(
        username=point_system_data.username,
        total_points=point_system_data.total_points,
        date_point=point_system_data.date_point
    )
    
    # Menyimpan objek PointSystem ke database
    db.add(point_system)
    db.commit()
    db.refresh(point_system)
    
    return point_system
