from fastapi import APIRouter,HTTPException,status,Depends
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from models import Request,Event
from routers.auth import get_current_user
import models

app=APIRouter()


router = APIRouter(
    prefix="/approval",
    tags=["approval"]
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


@router.get("/sent_requests/")
def event_approval_requests(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        query = db.query(Event)\
                .filter(Event.event_owner_id== user.get("user_id")).all()
        if query is None:
            return {"message": "no Requests found", "status": status.HTTP_404_NOT_FOUND}

        return {"message": "successful", "data": query, "status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/received_requests/")
async def received_event_request(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        query= [db.query(Request).filter(
            Request.user_id == user.get("user_id")).all()]

        if query is None:
            return {"message": "no Requests found", "status": status.HTTP_404_NOT_FOUND}

        return {"message": "successful", "data": query, "status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/received_requests/{id}/{num}")
async def update_event_request(id: int, num:int ,db: Session = Depends(get_db), user: dict = Depends(get_current_user)):

        event_request = db.query(Event).get(id)
        if event_request is None:
            raise HTTPException(status_code=404,detail=" request not found")

        if event_request.event_owner_id == user.get("user_id"):
            raise HTTPException(status_code=403, detail="You are not allowed to update this request")

        if num == 0:
            event_request.approval = "rejected"
        else:
            event_request.approval = "approved"
        db.commit()
        return {"message":"updated approval successfully", "status": status.HTTP_200_OK}