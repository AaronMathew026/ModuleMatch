from pydantic import BaseModel


class UserProfile(BaseModel):
    name : str
    year : int
    course : str 
    interests: list[str]
    goals: str






