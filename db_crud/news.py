from sqlalchemy.orm import Session

from models import asah_models
from schemas.news import NewsRead

def get_all_news(db: Session):
    news = db.query(asah_models.News).all()
    return [NewsRead(
        news_id=n.news_id,
        title=n.title,
        content=n.content,
        author=n.author,
        date_news=n.date_news,
        thumbnail=n.thumbnail,
        url=n.url
    ) for n in news]

def get_news_by_id(db: Session, news_id: int):
    news = db.query(asah_models.News).filter(asah_models.News.news_id == news_id).first()
    if not news:
        return None
    return NewsRead(
        news_id=news.news_id,
        title=news.title,
        content=news.content,
        author=news.author,
        date_news=news.date_news,
        thumbnail=news.thumbnail,
        url=news.url
    )
