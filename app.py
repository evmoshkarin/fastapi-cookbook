from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Recipe
from schemas import MessageResponse, RecipeCreate, RecipeDetailResponse, RecipeListItem

app = FastAPI(
    title="Кулинарная книга API",
    description="""
    Документация API для кулинарной книги.

    Возможности:
    - GET /recipes — получить список всех рецептов
    - GET /recipes/{recipe_id} — получить детальную информацию о рецепте
    - POST /recipes — создать новый рецепт
    """,
    version="1.0.0",
)


app.get("/", response_model=MessageResponse)


async def root():
    return {"message": "Добро пожаловать в Кулинарную книгу API!", "recipe_id": None}


@app.get("/", response_model=MessageResponse)
async def root():
    return {"message": "Добро пожаловать в Кулинарную книгу API!", "recipe_id": None}


@app.get("/recipes", response_model=List[RecipeListItem])
def get_recipes(db: Session = Depends(get_db)):
    recipes = (
        db.query(Recipe).order_by(Recipe.views.desc(), Recipe.cooking_time.asc()).all()
    )
    return recipes


@app.get("/recipes/{recipe_id}", response_model=RecipeDetailResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рецепт с ID {recipe_id} не найден",
        )

    recipe.views = recipe.views + 1  # type: ignore[assignment]
    db.commit()
    db.refresh(recipe)

    ingredients_list = recipe.ingredients.split(",")

    return {
        "id": recipe.id,
        "title": recipe.title,
        "cooking_time": recipe.cooking_time,
        "views": recipe.views,
        "ingredients": ingredients_list,
        "description": recipe.description,
    }


@app.post(
    "/recipes", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
def create_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db)):
    ingredients_str = ",".join(recipe_data.ingredients)

    new_recipe = Recipe(
        title=recipe_data.title,
        cooking_time=recipe_data.cooking_time,
        ingredients=ingredients_str,
        description=recipe_data.description,
        views=0,
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return MessageResponse(
        message=f"Рецепт '{recipe_data.title}' успешно создан",
        recipe_id=int(new_recipe.id),
    )


@app.get("/health", response_model=MessageResponse)
async def health_check():
    return {"message": "API работает нормально", "recipe_id": None}
