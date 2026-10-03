from pydantic import BaseModel, Field


class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)


class ProductUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = Field(None, gt=0)


