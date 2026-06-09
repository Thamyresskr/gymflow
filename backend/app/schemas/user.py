from pydantic import BaseModel


class UserCreate(BaseModel):
    nome: str
    email: str
    senha: str


class UserResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True