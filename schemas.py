from pydantic import BaseModel, Field
from typing import List, Optional


class RecipeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название блюда")
    cooking_time: int = Field(..., gt=0, description="Время приготовления в минутах")
    ingredients: List[str] = Field(..., description="Список ингредиентов")
    description: str = Field(..., min_length=1, description="Описание приготовления")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Оливье",
                "cooking_time": 60,
                "ingredients": ["картофель", "морковь", "колбаса", "горошек", "майонез"],
                "description": "Отварить овощи, нарезать кубиками, смешать с майонезом..."
            }
        }


class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    id: int
    views: int

    class Config:
        from_attributes = True


class RecipeListItem(BaseModel):
    id: int
    title: str
    cooking_time: int
    views: int

    class Config:
        from_attributes = True


class RecipeDetailResponse(BaseModel):
    id: int
    title: str
    cooking_time: int
    views: int
    ingredients: List[str]
    description: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
    recipe_id: Optional[int] = None
