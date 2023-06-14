from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    username = Column(String(50), primary_key=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    date_user = Column(Date)

    scan_histories = relationship('ScanHistory', back_populates='user')
    point_system = relationship('PointSystem', uselist=False, back_populates='user')

class ScanHistory(Base):
    __tablename__ = 'scan_history'

    waste_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), ForeignKey('user.username'))
    date_scan = Column(Date)
    prediction_waste = Column(String)
    accuracy_percentage = Column(String)
    message = Column(String(5000))
    recycle_recommendation = Column(String)
    action = Column(String)
    gcs_image_path = Column(String)

    user = relationship('User', back_populates='scan_histories')

class PointSystem(Base):
    __tablename__ = 'point_system'

    point_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), ForeignKey('user.username'), unique=True)
    total_points = Column(Integer)
    date_point = Column(Date)

    user = relationship('User', back_populates='point_system')

class News(Base):
    __tablename__ = 'news'

    news_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    content = Column(Text)
    author = Column(String(100))
    date_news = Column(Date)
    thumbnail = Column(String(255))
    url = Column(String(255))
