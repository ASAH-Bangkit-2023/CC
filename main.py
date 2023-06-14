from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File, Form, APIRouter
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from config.db import engine, get_db
from models import asah_models
from db_crud.user import *
from db_crud.news import get_news_by_id, get_all_news
from db_crud.point_system import create_point_system
from db_crud.scan_waste import create_waste_scan
from db_crud.scan_history import get_scan_history, get_scan, delete_scan
from schemas.user import UserOut, UserAuth, UserDB
from schemas.token import TokenSchema
from schemas.news import NewsBase, NewsRead
from schemas.point_system import PointSystemCreate
from schemas.scan_waste import WasteScanCreate
from storage.gcs import GCStorage
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from auth.utils import *
from auth.deps import get_current_user
from typing import List
from datetime import date, datetime
from tfmodel.predict import predict_image_classes

asah_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ASAH",
    version="0.1"
)

auth_router = APIRouter(
    prefix="/auth"
)

scan_router = APIRouter(
    prefix="/scan_waste"
)

point_router = APIRouter(
    prefix="/point"
)

news_router = APIRouter(
    prefix="/news",
    dependencies=[Depends(get_current_user)]
)

@app.get("/", include_in_schema=False)
def redirect_docs():
    return RedirectResponse("/docs")


# Auth 

@auth_router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, db: Session = Depends(get_db)):
    # check if username already exists
    existing_user = getUser(db, data.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    elif getEmail(db, data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already used"
    )
    
    print("Creating new user")
          
    # create a new user
    new_user = UserDB(
        full_name=data.full_name,
        username=data.username,
        email=data.email,
        hashed_password=get_hashed_password(data.password),
        date_user=datetime.now()
    )

    createUser(db, new_user)

    # create point system for the new user
    point_system_data = PointSystemCreate(username=new_user.username, total_points=0, date_point=date.today())
    
    create_point_system(db, point_system_data)

    return new_user

@auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = getUsername(db, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username"
        )

    hashed_pass = getHashedPassword(db, user)
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    return {
        "access_token": create_access_token(getUsername(db, user)),
        "refresh_token": create_refresh_token(getUsername(db, user)),
    }


@auth_router.get('/profile', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    result = getUser(db, user.username)
    return result

# Endpoint to delete profile by username, password, and password_confirmation
@auth_router.delete('/profile/delete/{username}', summary="Delete account by user")
async def delete_profile(username: str, password: str, password_confirmation: str, user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(asah_models.User).filter(asah_models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if password != password_confirmation:
        raise HTTPException(status_code=400, detail="Password confirmation does not match")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    db.delete(user)
    db.commit()
    return {"message": "Profile successfully deleted"}

# Scan

# endpoint for scanning waste
@scan_router.post("/", summary="Scan waste")
async def scan_waste(file:UploadFile=File(...), user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):

    predictions = predict_image_classes(file.file.read())

    for i, info_dict in enumerate(predictions):
        prediction = info_dict['prediction']
        accuracy_percentage = info_dict['accuracy_percentage']
        message = info_dict['message']
        
        # Use dict.get() method with a default value for missing keys
        recycle_recommendation = info_dict.get('recycle_recommendation')
        action = info_dict.get('action')

        if prediction == 'No class detected':
            recycle_recommendation = None
            action = None

    # Reset the stream position to the beginning before uploading
    await file.seek(0)

    # Save the scanned image to Google Cloud Storage
    gcs_image_path = GCStorage().upload_file(file.file, file.filename)

    newWasteScan = WasteScanCreate(
        username=user_details.username,
        prediction_waste=prediction,
        date_scan=datetime.now(),
        accuracy_percentage=accuracy_percentage,
        message = message,
        recycle_recommendation=recycle_recommendation,
        action=action,
        gcs_image_path=gcs_image_path
    )

    # create a new waste scan in the database
    scan = create_waste_scan(db=db, waste=newWasteScan)
    return scan

# endpoint for getting all history scans for a user
@scan_router.get("/history", summary="Scan history")
def get_scan_history_endpoints(user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    print(user_details.username)
    history = get_scan_history(db=db, username = user_details.username)
    return history

# endpoint for getting a single scan history entry
@scan_router.get("/{waste_id}", summary="Get a history by waste_id")
def get_scan_endpoints(waste_id: int, user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = get_scan(db=db, username=user_details.username, waste_id=waste_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

# endpoint for deleting a scan history entry
@scan_router.delete("/delete/{waste_id}", summary="Delete a history")
def delete_scan_history_entry(waste_id: int, user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_scan(db=db, username=user_details.username, waste_id=waste_id)
    return {"message": "Scan successfully deleted"}

# Point

@point_router.post("/add", summary="Add point")
async def add_points(points: int, user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(asah_models.User).filter(asah_models.User.username == user_details.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    point_system = user.point_system
    point_system.total_points += points
    db.commit()

    return {"username": user_details.username, "added_points": points, "total_points": point_system.total_points}

@point_router.get("/check", summary="Check point")
async def get_points(user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(asah_models.User).filter(asah_models.User.username == user_details.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    point_system = user.point_system
    # if point_system is None:
    #     raise HTTPException(status_code=404, detail="Your point is 0")

    return {"username": user_details.username, "total_points": point_system.total_points}

@point_router.delete("/redeem", summary="Redeem point")
async def redeem_points(points: int, user_details: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(asah_models.User).filter(asah_models.User.username == user_details.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    point_system = user.point_system
    # if point_system is None:
    #     raise HTTPException(status_code=404, detail="Your points is 0")
    
    if point_system.total_points < points:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    point_system.total_points -= points
    db.commit()

    return {"username": user_details.username, "reduced_points": points, "total_points": point_system.total_points}

# News

# Endpoint to get all news
@news_router.get("/", summary="Get news", response_model=List[NewsRead])
def get_all_news_endpoint(db: Session = Depends(get_db)): # Tidak boleh sama nama fungsi endpoint-nya dengan nama model
    news_result = get_all_news(db)
    return news_result

# Endpoint to get news by id or url
@news_router.get("/{news_id}", summary="Get news by news_id", response_model=NewsBase)
def get_news_by_id_endpoint(news_id: int, db: Session = Depends(get_db)):
    news_result = get_news_by_id(db, news_id)
    if not news_result:
        raise HTTPException(status_code=404, detail="News not found")
    return news_result


app.include_router(auth_router, tags=["auth"])
app.include_router(scan_router, tags=["scan_waste"])
app.include_router(point_router, tags=["point"])
app.include_router(news_router, tags=["news"])


app.add_middleware(
    CORSMiddleware,
    #allow_origins=['url'],
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)