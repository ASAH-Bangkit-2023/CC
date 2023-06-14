FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV PORT 1234
ENV MYSQL_URL "mysql+pymysql://root:password@IP:3306/db-name"
ENV JWT_SECRET_KEY "SECRET"  
ENV JWT_REFRESH_SECRET_KEY "SECRET" 

RUN pip install --no-cache-dir -r requirements.txt

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}