from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)
    hashed_password = Column(String)

    event = relationship("Event", back_populates="event_owner")

    participants = relationship("Participant", back_populates="pt_user", foreign_keys="[Participant.pt_id]")
    # participants_name = relationship("Participant", back_populates="pt_name", foreign_keys="[Participant.ptn_name]")
    # participants_email = relationship("Participant", back_populates="pt_email", foreign_keys="[Participant.pte_email]")
    request = relationship("Request", back_populates="user")


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    event_owner_id = Column(Integer, ForeignKey('users.id'))
    event_name = Column(String)
    duration = Column(String)
    event_place = Column(String)
    price = Column(Integer)
    event_outcome = Column(String)
    event_description = Column(String)
    attachments = Column(String)
    approval = Column(String, default="pending")
    no_of_participants=Column(Integer,default=0)

    event_owner = relationship("User", back_populates="event")
    participants = relationship("Participant", back_populates="pt_event")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    pt_event_id = Column(Integer, ForeignKey("event.id"))
    pt_id = Column(Integer, ForeignKey("users.id"))
    # ptn_name = Column(String, ForeignKey("users.username"))
    # pte_email = Column(String, ForeignKey("users.email"))

    pt_user = relationship("User", back_populates="participants", foreign_keys="[Participant.pt_id]")
    # pt_name = relationship("User", back_populates="participants_name", foreign_keys="[Participant.ptn_name]")
    # pt_email = relationship("User", back_populates="participants_email", foreign_keys="[Participant.pte_email]")
    pt_event = relationship("Event", back_populates="participants")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String)

    user = relationship("User", back_populates="request")
