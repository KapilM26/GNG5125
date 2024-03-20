from pydantic import BaseModel


class Beer(BaseModel):
    id: int
    name: str
    alcohol_content: float
    flavor: str
    packing: str
    user_rating: float
    region: str
    season: str


    class Config:
        orm_mode = True
