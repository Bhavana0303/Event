from fastapi import APIRouter,HTTPException,status,UploadFile,Form,File,Depends
from pydantic import BaseModel
from typing import List
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from models import Event,Participant,Request,User
from routers.auth import get_current_user
import models
import os

app=APIRouter()


router = APIRouter(
    prefix="/events",
    tags=["events"]
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


class CreateEvent(BaseModel):
    event_name:str
    duration:str
    event_place:str
    price:int
    event_outcome:str
    event_description:str
    attachments:str


def send_request(db,id):
    admin_users = db.query(models.User).filter(models.User.role == 'admin').all()

    for admin_user in admin_users:
        request = Request(
            user_id=admin_user.id,
            message=f"New event (ID: {id}) needs approval.",
        )
        db.add(request)

    db.commit()


@router.post("/create_event")
async def create_event(
        event_name: str = Form(...),
        duration: str = Form(...),
        event_place: str = Form(...),
        price: int = Form(...),
        event_outcome: str = Form(...),
        event_description: str = Form(...),
        attachments: str = Form(...),
                                user: dict = Depends(get_current_user),
                                db: Session = Depends(get_db),
                                attachment_files : List[UploadFile] = File(...),
                                ):
    try:
        UPLOAD_FOLDER = "attachments/events/" + str(user['user_id'])

        event_model = Event()
        event_model.event_owner_id = user.get("user_id")
        event_model.event_name = event_name
        event_model.duration=duration
        event_model.event_place=event_place
        event_model.price = price
        event_model.event_outcome = event_outcome
        event_model.event_description = event_description
        event_model.attachments= attachments

        db.add(event_model)
        print(event_model)
        db.commit()

        product_folder_path = os.path.join(UPLOAD_FOLDER, str(event_model.id))
        os.makedirs(product_folder_path, exist_ok=True)
        saved_image_paths = []

        for attachment in attachment_files:
            attachment_path = os.path.join(product_folder_path, attachment.filename)
            with open(attachment_path, "wb") as attachment_file:
                attachment_file.write(attachment.file.read())
            saved_image_paths.append(attachment_path)
        event_model.attachments = product_folder_path  # storing the path
        db.commit()
        send_request(db,event_model.id)
        return {"message": "Created event Successfully ",
                "status_code": status.HTTP_201_CREATED}
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/all_events")
async def get_all_events(db: Session = Depends(get_db)):
    try:
        query=db.query(Event).all()
        if query is None:
         return {"message": "no events found", "status": status.HTTP_404_NOT_FOUND}

        return {"message": "successful", "data": query, "status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/events/by_id/{id}")
async def get_event_by_id(id: int, db: Session = Depends(get_db)):
    try:
        get_event = db.query(Event).filter(Event.id == id).first()

        if get_event is None:
            raise HTTPException(status_code=404, detail="no events found")

        return {"message": "successful", "data": get_event, "status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


# @router.post("/participate/{id}")
# async def participate_in_event(id:int,user: dict = Depends(get_current_user),
#                                db: Session = Depends(get_db)):
#     try:
#         event = db.query(Event).filter(Event.id == id).first()
#
#         if event is None:
#             raise HTTPException(status_code=404, detail="no events found")
#         participation = db.query(Participant.pt_event_id==id,
#                                  Participant.pt_id==user.get(id)).first()
#         db.add(participation)
#         db.commit()
#
#         event.no_of_participants += 1
#
#         return {"message": "You have successfully participated in this event", "status": status.HTTP_200_OK}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
#
@router.post("/participate/{id}")
async def participate_in_event(id: int,user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # try:
        event = db.query(Event).filter(Event.id == id).first()

        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        # Check if the user is already a participant in the event
        is_participant = db.query(Participant).filter(
            Participant.pt_event_id == id,
            Participant.pt_id == user['user_id']
        ).first()

        if is_participant:
            raise HTTPException(status_code=400, detail="You are already a participant in this event")

        # Add the user as a participant
        new_participant = Participant(
            pt_event_id=id,
            pt_id=user.get('user_id')
        )
        db.add(new_participant)

        # Update the number of participants for the event
        event.no_of_participants += 1

        db.commit()

        return {"message": "You have successfully participated in this event", "status": status.HTTP_200_OK}
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #


