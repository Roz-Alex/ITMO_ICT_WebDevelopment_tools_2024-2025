from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


# Enums for better usability
class Gender(Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class TravelStyle(Enum):
    camping = "Camping"
    active = "Active"
    cultural = "Cultural"
    comfort = "Comfort"

class ParticipationStatus(Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

# Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    pass_hash: str
    age: Optional[int] = None
    gender: Optional[Gender] = None
    country: Optional[str] = None
    travel_style: Optional[TravelStyle] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    trips_created: List["Trip"] = Relationship(back_populates="creator")
    trip_requests: List["TripParticipant"] = Relationship(back_populates="user")
    user_interests: List["UserInterest"] = Relationship(back_populates="user")


class Interest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    users: List["UserInterest"] = Relationship(back_populates="interest")


class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creator_id: int = Field(foreign_key="user.id")
    title: str
    description: Optional[str] = None
    destination: str
    start_date: date
    end_date: date
    budget: Optional[float] = None
    transport: Optional[str] = None
    max_participants: Optional[int] = None
    status: str = "active"

    creator: Optional[User] = Relationship(back_populates="trips_created")
    participants: List["TripParticipant"] = Relationship(back_populates="trip")


class TripParticipant(SQLModel, table=True):
    trip_id: int = Field(foreign_key="trip.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    status: ParticipationStatus = ParticipationStatus.pending
    message: Optional[str] = None
    joined_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="trip_requests")
    trip: Optional[Trip] = Relationship(back_populates="participants")


class UserInterest(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    interest_id: int = Field(foreign_key="interest.id", primary_key=True)
    level: Optional[int] = None

    user: Optional[User] = Relationship(back_populates="user_interests")
    interest: Optional[Interest] = Relationship(back_populates="users")
