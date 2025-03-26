from pydantic import BaseModel, Field
from typing import List, Optional


class Preferences(BaseModel):
    brands: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)


class UserData(BaseModel):
    user_id: Optional[int]
    location: Optional[str] = "US"


class RecommendationRequest(BaseModel):
    top_n: Optional[int] = 4
    user: UserData


class Product(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    price: float


class RecommendationResponse(BaseModel):
    status: str
    message: str
    data: dict  # You can replace with a structured Product list if needed
